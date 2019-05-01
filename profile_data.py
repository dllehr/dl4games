import numpy as np
import cv2
import argparse
import sys
import time
import os
import yaml

w = np.array([1,0,0,0,0,0,0])
s = np.array([0,1,0,0,0,0,0])
a = np.array([0,0,1,0,0,0,0])
d = np.array([0,0,0,1,0,0,0])
j = np.array([0,0,0,0,1,0,0])
k = np.array([0,0,0,0,0,1,0])
nk = np.array([0,0,0,0,0,0,1])
keys = ['w', 's', 'a', 'd', 'j', 'k', 'nk']

def go_display_images(X):
    index = 0
    m = X.shape[0]
    cv2.imshow('window',X[index])
    while True:
        k = cv2.waitKey(25) & 0xFF
        if k == -1:
            continue
        elif k == ord('q'):
            cv2.destroyAllWindows()
            break
        elif k == ord('m'):
            index += 1
            if(index >= m):
                print ("WARNING: Can't go forward any further")
                continue

        #cv2.destroyAllWindows()
            cv2.imshow('window',X[index])
            print("Index = " + str(index))
        elif k == ord('n'):
            index -= 1
            if(index < - m):
                print ("WARNING: Can't go back any further")
                continue

            cv2.imshow('window',X[index])
            print("Index = " + str(index))

def calculate_Y(y):
    print("calculate_Y")
    m = y.shape[0]
    print("Total Frames: {}".format(m))
    move_count = np.array([0,0,0,0,0,0,0])
    for i in y:
        move_count = move_count + i
    print("Keys\tcount\tpercent_active:")
    for idx, val in enumerate(move_count):
        print("{}\t{}\t{}".format(keys[idx],val, val*100.0/m))
def main():

    parser = argparse.ArgumentParser(description='Training for game recording')
    parser.add_argument('-s', help='single file', action="store_true", default=False)
    parser.add_argument('--height', help='height of model', dest='height', type=int, default=-1)
    parser.add_argument('--width', help='width of model', dest='width', type=int, default=-1)
    parser.add_argument('-n', help='dataset name', dest='ds_name', type=str)
    parser.add_argument('-d', help='display images', action="store_true", default=False)
    args = parser.parse_args()

    # iterates through the training files
    starting_value=1
    count=0
    single_file = args.s
    display_images = args.d

    if(single_file):
        if(args.width == -1 or args.height == -1):
            print("ERROR: You must specify height and width when using single file")
            return -1
        width = args.width
        height = args.height
    else:
        meta_file = '{}.meta'.format(args.ds_name)
        if os.path.isfile(meta_file):
            with open(meta_file, 'r') as stream:
                data_loaded = yaml.load(stream)
            height = data_loaded['height']
            width = data_loaded['width']
        else:
            print("ERROR: Loading string of input data requires a .meta file")
            return -1

    while True:
    #file_name = 'training_data-{}.npy'.format(starting_value)
        if (single_file):
            file_name = args.ds_name
        else:
            file_name = '{}-{}.npy'.format(args.ds_name, starting_value)
        if os.path.isfile(file_name):
            print("File {} exists, adding".format(file_name))
            train_data = np.load(file_name)
            np.random.shuffle(train_data)
            starting_value += 1
            if count == 0:
                print('count is zero')
                total_train_data = train_data
                count += 1
            else:
                total_train_data = np.concatenate((total_train_data,train_data))
            if(single_file):
                break
        else:
            print("File {} does not exists, stopping".format(file_name))
            break

    #X = np.array([i[0] for i in total_train_data]).reshape(-1,width,height,3)
    #experiment, change up width and height, as original array is height, width
    m = total_train_data.shape[0]
    X = np.array([i[0] for i in total_train_data]).reshape(-1,height,width,3)
    y = np.array([i[1] for i in total_train_data])
    print ("X Shape: \t" + str(X.shape))
    print ("Y Shape: \t" + str(y.shape))
    calculate_Y(y)
    if (display_images):
        go_display_images(X)



main()
