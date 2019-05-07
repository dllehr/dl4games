import numpy as np
import cv2
import argparse
import sys
import time
import os
import yaml
from utils import load_dataset

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
    parser.add_argument('--height', help='height of model', dest='height', type=int, default=None)
    parser.add_argument('--width', help='width of model', dest='width', type=int, default=None)
    parser.add_argument('-n', help='dataset name', dest='ds_name', type=str)
    parser.add_argument('-d', help='display images', action="store_true", default=False)
    args = parser.parse_args()

    single_file = args.s
    display_images = args.d

    X, y = load_dataset(args.ds_name, single_file, args.height, args.width )

    print ("X Shape: \t" + str(X.shape))
    print ("Y Shape: \t" + str(y.shape))
    calculate_Y(y)
    if (display_images):
        go_display_images(X)



main()
