import numpy as np
from grabscreen import grab_screen
from directkeys import PressKey,ReleaseKey, W, A, S, D, J, K
import argparse
import cv2
import time
from getkeys import key_check
import os
import sys
import utils
import yaml
import platform
if platform.system() == "Windows":
    import winGuiAuto as wh
import win32gui
from models2 import driving_model

w = np.array([1,0,0,0,0,0,0])
s = np.array([0,1,0,0,0,0,0])
a = np.array([0,0,1,0,0,0,0])
d = np.array([0,0,0,1,0,0,0])
j = np.array([0,0,0,0,1,0,0])
k = np.array([0,0,0,0,0,1,0])
nk = np.array([0,0,0,0,0,0,1])
w_hit = np.argmax(w)
s_hit = np.argmax(s)
a_hit = np.argmax(a)
d_hit = np.argmax(d)
j_hit = np.argmax(j)
k_hit = np.argmax(k)
nk_hit = np.argmax(nk)
starting_value = 1

# On a 1920x1080 Screen
# Required cropping to remove Windows handle and edges
TOP_BORDER_SIZE=55
EDGE_BORDER_SIZE=10

'''
Remove the window edges and Menu from top before resizing
'''
def remove_border(obj):
    lst = list(obj)
    lst[0] = lst[0]+EDGE_BORDER_SIZE
    lst[1] = lst[1]+TOP_BORDER_SIZE
    lst[2] = lst[2]-EDGE_BORDER_SIZE
    lst[3] = lst[3]-EDGE_BORDER_SIZE
    obj = tuple(lst)
    return obj

def left():
    if random.randrange(0,3) == 1:
        PressKey(W)
    else:
        ReleaseKey(W)
    PressKey(A)
    ReleaseKey(S)
    ReleaseKey(D)
    #ReleaseKey(S)

def right():
    if random.randrange(0,3) == 1:
        PressKey(W)
    else:
        ReleaseKey(W)
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(S)

def keys_to_move(keys):
    if keys[a_hit]:
        PressKey(A)
    else:
        ReleaseKey(A)

    if keys[d_hit]:
        PressKey(D)
    else:
        ReleaseKey(D)

    if keys[w_hit]:
        PressKey(W)
    else:
        ReleaseKey(W)

    if keys[s_hit]:
        PressKey(S)
    else:
        ReleaseKey(S)


    if keys[j_hit]:
        PressKey(J)
    else:
        ReleaseKey(J)

    if keys[k_hit]:
        PressKey(K)
    else:
        ReleaseKey(K)
def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''
    output = np.array([0,0,0,0,0,0,0])
    if 'W' in keys:
        output += w
    if 'A' in keys:
        output += a
    if 'S' in keys:
        output += s
    if 'D' in keys:
        output += d
    if 'J' in keys:
        output += j
    if 'K' in keys:
        output += k

    if(not np.count_nonzero(output)):
        output = nk

    #print(output)
    return output

def main():
    print(platform.system())
    delim = "/" if os.name == "posix" else "\\"
    debug = False
    parser = argparse.ArgumentParser(description='Training for game recording')
    parser.add_argument('-t', help='game_template',         dest='game_template',  type=str,   default='default')
    parser.add_argument('-c', help='config file',           dest='config_file',    type=str,   default='config.yml')
    parser.add_argument('-o', help='model output dir',      dest='model_dir',      type=str,   default='model')
    parser.add_argument('-d', help='data output directory', dest='data_dir',       type=str)
    parser.add_argument('--width', help='screen capture width',  dest='width',          type=int)
    parser.add_argument('--height', help='screen capture height', dest='height',         type=int)

    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    cfg = utils.load_cfg(args.config_file, args.game_template)

    data_dir = args.data_dir if args.data_dir else cfg['data_dir']

    width = args.width if args.width else cfg['width']
    height = args.height if args.height else cfg['height']
    crop_bottom = cfg['crop']['bottom']
    crop_top = cfg['crop']['top']
    crop_left = cfg['crop']['left']
    crop_right = cfg['crop']['right']
    recording_window = cfg['window_handle']
    debug = args.debug
    #model_name = args.model_name
    

    #con = Config(config_file, model_name)
   
    target_name = data_dir + delim + args.game_template
    starting_value=1
 
    hwnd = wh.findTopWindow(recording_window)
    rect = wh.GetWindowPlacement(hwnd)[-1]

    

    print("Template: {}".format(args.game_template))
    #image = ImageGrab.grab(rect)
    while True:
    #file_name = 'training_data-{}.npy'.format(starting_value)
        file_name = '{}-{}.npy'.format(target_name, starting_value)
        if os.path.isfile(file_name):
            print("File {} exists, moving along".format(file_name))
            starting_value += 1
        else:
            print("File {} does not exists, starting here".format(file_name))
            break

    starting_value = starting_value
    training_data = []
    for i in list(range(2))[::-1]:
        print(i+1)
        time.sleep(1)

    last_time = time.time()
    paused = False
    print('STARTING!!!')
    if os.path.isfile('{}.meta'.format(target_name)):
        with open('{}.meta'.format(target_name), 'r') as stream:
            data_loaded = yaml.load(stream)
        model_height = data_loaded['height']
        model_width = data_loaded['width']


    LR=0.1
    print("MODEL WIDTH {}".format(model_width))
    model = driving_model(model_width, model_height, 3, LR, output=7)

    model.load_weights("po.checkpoint")
    
    print("WINDOW PLACEMENT {}".format(wh.GetWindowPlacement(hwnd)))
    while(True):
        rect = remove_border(wh.GetWindowPlacement(hwnd)[-1])
        if not paused:
            screen = grab_screen(region=rect)
            last_time = time.time()
            # resize to something a bit more acceptable for a CNN
            screen = cv2.resize(screen, (width, height))
            
            #print ("screen {}".format(screen))
            screen = screen[crop_top:height-crop_bottom, crop_left:width-crop_right]
            # run a color convert:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            prediction = model.predict(np.expand_dims(screen,axis=0))[0] + .2
            print("prediction {}".format(np.around(prediction, decimals=1)))
            keys_to_move(np.rint(prediction).astype(int))
            
        keys = key_check()
        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)
        if 'Q' in keys:
            return


main()
