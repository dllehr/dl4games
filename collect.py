import numpy as np
import argparse
import cv2
import time

import os
import sys
import utils
import yaml
import platform
import matplotlib.pyplot as plt

if platform.system() == "Windows":
    from getkeys import key_check
    from grabscreen import grab_screen    
    import winGuiAuto as wh
    import win32gui
else:
    import winLinux as wh
    from linkeylisten import KeyListener
    from grabscreenLinux import grab_screen
    from lingetkeys import key_check


w = np.array([1,0,0,0,0,0,0])
s = np.array([0,1,0,0,0,0,0])
a = np.array([0,0,1,0,0,0,0])
d = np.array([0,0,0,1,0,0,0])
j = np.array([0,0,0,0,1,0,0])
k = np.array([0,0,0,0,0,1,0])
nk = np.array([0,0,0,0,0,0,1])

starting_value = 1

# On a 1920x1080 Screen
# Required cropping to remove Windows handle and edges
TOP_BORDER_SIZE=55
EDGE_BORDER_SIZE=10
paused=False
quitting=False

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

def keys_to_output(keys):
    '''
    Convert keys to a ...multi-hot... array
     0  1  2  3  4   5   6   7    8
    [W, S, A, D, WA, WD, SA, SD, NOKEY] boolean values.
    '''
    output = np.array([0,0,0,0,0,0,0])
    if 'w' in keys:
        output += w
    if 'a' in keys:
        output += a
    if 's' in keys:
        output += s
    if 'd' in keys:
        output += d
    if 'j' in keys:
        output += j
    if 'k' in keys:
        output += k

    if(not np.count_nonzero(output)):
        output = nk

    #print(output)
    return output

def key_pressed(kc):
    return
    #print ("Key pressed - keycode: %d" % kc)

def key_released(kc):
    return
    #print ("Key released - keycode: %d" % kc)

def toggle_pause():
    global paused
    if paused:
        paused = False
        print('unpaused!')
        time.sleep(1)
    else:
        print('Pausing!')
        paused = True
        time.sleep(1)

def quit():
    global quitting
    quitting=True
    
def main():
    global paused, quitting
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
    recording_window="Slack"
    print("RECORDING_WINDOW {}".format(recording_window))
    hwnd = wh.findTopWindow(recording_window)
    #rect = wh.GetWindowPlacement(hwnd)[-1]
    rect = wh.GetWindowPlacement(hwnd)
    print("rect {}".format(rect))

    print("Template: {}".format(args.game_template))
    if platform.system() != "Windows":
        kl = KeyListener()
        kl.register_pause(toggle_pause)
        kl.register_quit(quit)
        kl.start()
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
    print('STARTING!!!')
    meta_info = dict(
        name = args.game_template,
        height = height-crop_bottom - crop_top,
        width = width-crop_left-crop_right,
    )
    with open('{}.meta'.format(target_name), 'w') as outfile:
        yaml.dump(meta_info, outfile, default_flow_style=False)

    while(True):
        #rect = remove_border(wh.GetWindowPlacement(hwnd))
        rect = wh.GetWindowPlacement(hwnd)
        #print("RECT PLACEMENT: {}".format(rect))
        keys = key_check(kl)
        last_time = time.time()
        if not paused:
            before_grab_time = time.time()
            screen = grab_screen(region=rect)
            print('grab took {} seconds'.format(time.time()-before_grab_time))
            
            # resize to something a bit more acceptable for a CNN
            screen = cv2.resize(screen, (width, height))
            #print("SHape of screen: " + str(screen.shape))
            #print ("screen {}".format(screen))
            screen = screen[crop_top:height-crop_bottom, crop_left:width+crop_left]
            # run a color convert:
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            #keys = key_check(kl)
            output = keys_to_output(keys)
            #print("output {}".format(output))
                 #if np.count_nonzero(output & d):
                    #    print("Found d key")
            training_data.append([screen,output])

            print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
            #cv2.imshow('window',cv2.resize(screen,(640,360)))
            if(debug):
                plt.ion()
                fig, ax = plt.subplots()
                ax.imshow('window',img)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

            if len(training_data) % 100 == 0:
                print('loop took {} seconds'.format(time.time()-last_time))
                print(len(training_data))

                if len(training_data) == 500 and not debug:
                    file_name = '{}-{}.npy'.format(target_name, starting_value)
                    np.save(file_name,training_data)
                    print('SAVED')
                    training_data = []
                    starting_value += 1
                    #file_name = 'X:/pygta5/phase7-larger-color/training_data-{}.npy'.format(starting_value)
        if quitting:
            kl.exit()
            return


main()
