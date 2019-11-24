import numpy as np
import cv2
import argparse
import sys
import time
import os
import pandas as pd
import yaml
from sklearn.model_selection import train_test_split #to split out training and testing data 
from collections import deque
from models2 import driving_model
from random import shuffle
from utils import Config

FILE_I_END = 49

LR = 1e-3
LR = 1e-4
#LR = 1e-5
EPOCHS = 20

w = np.array([1,0,0,0,0,0,0])
s = np.array([0,1,0,0,0,0,0])
a = np.array([0,0,1,0,0,0,0])
d = np.array([0,0,0,1,0,0,0])
j = np.array([0,0,0,0,1,0,0])
k = np.array([0,0,0,0,0,1,0])
nk = np.array([0,0,0,0,0,0,1])

DATA_DIR="data"
def create_action_move(all_inputs):
    action = [i[4:6] for i in all_inputs]
    move = [i[:4] for i in all_inputs]

    for i in range(len(all_inputs)):
        #print("I    {}".format(i[1]))
        if np.count_nonzero(action[i]):
            action[i] = np.append(action[i], 0)
        else:
            action[i] = np.append(action[i], 1)

        if np.count_nonzero(move[i]):
            move[i] = np.append(move[i], 0)
        else:
            move[i] = np.append(move[i], 1)    
    return move, action

def train_model(model_name, model_vers, outputs, width, height, X, y, X_valid, y_valid, load_model=False):
    full_model = '/models/'+model_name+"-"+str(model_vers)+".checkpoint"
    def_model = '/models/'+model_name+".checkpoint"
    class_weights = {0:1,
                1:1,
                2:1,
                3:1,
                4:1,
                5:1,
                6:.5}
    class_weights = [1,1,1,1,1,1,.5]
              
    model = driving_model(width, height, 3, LR, output=outputs, model_name=model_name)
    if load_model:
        load_models = '/models/'+model_name+"-"+str(model_vers)+".checkpoint"
        model.load_weights(load_models)
        print('We have loaded a previous model!!!!')
    else:
        full_model = '/models/'+model_name+"-"+str(model_vers)+".checkpoint"
    #print('Training model {}'.format(model_name))
    #print('Training model shape{}'.format(X.shape))
    #print('Training out shape  {}'.format(y.shape))    
    #print('Training out shape  {}'.format(y))    
    #print('is equal {}'.format(np.array_equal(X[0], X[1])))
    for i in list(range(5))[::-1]:
        model.fit(X, y, validation_data=(X_valid,y_valid), verbose=1, epochs=EPOCHS)
        print('SAVIN MODEL!')
        model.save_weights(full_model)
        model.save_weights(def_model)

def main():
    delim = "/" if os.name == "posix" else "\\"
    data_dir =  DATA_DIR

    parser = argparse.ArgumentParser(description='Training for game recording')
    parser.add_argument('-t', help='training',              dest='train_set',          type=str,   default='both')
    parser.add_argument('-o', help='model output dir',      dest='model_dir',         type=str,   default='data')
    parser.add_argument('-d', help='data directory',        dest='data_dir',          type=str,   default='data')
    parser.add_argument('-m', help='model name',            dest='model_name',        type=str,   default='default')
    parser.add_argument('-c', help='config file',           dest='config_file',       type=str,   default='config.yml')
    args = parser.parse_args()

    model_name = args.model_name
    config_file = args.config_file

    full_model_name = args.data_dir + delim + model_name

    model_dir = args.model_dir
    config_file = args.config_file

    con = Config(config_file, model_name)

    width = con.width - con.crop_left - con.crop_right
    height = con.height - con.crop_top - con.crop_bottom

    meta_file = '{}.meta'.format(full_model_name)
    print ("FULL META FULE {}".format(meta_file))
    if os.path.isfile(meta_file):
        with open(meta_file, 'r') as stream:
            data_loaded = yaml.load(stream)
        height = data_loaded['height']
        width = data_loaded['width']
    print("width is {}".format(width))
    # iterates through the training files
    model_vers=1
    while True:
        num_of_files=0
        while True:
        #file_name = 'training_data-{}.npy'.format(starting_value)
            file_name = '{}-{}.npy'.format(full_model_name, num_of_files+1)
            if os.path.isfile(file_name):
                print('File exists, moving along',num_of_files)
                num_of_files += 1
            else:
                print('File does not exist, starting fresh!',num_of_files)
                break

        
        data_order = [i for i in range(1,num_of_files+1)]
        shuffle(data_order)
        total_X = None
        total_Y= None
        total_test_x = None
        total_test_y = None

        for count,i in enumerate(data_order):
            file_name = '{}-{}.npy'.format(full_model_name, i)
            # full file info
            train_data = np.load(file_name)
            np.random.shuffle(train_data)
            print('{}'.format(file_name),train_data.shape)
            if count == 0:
                print('count is zero')
                total_train_data = train_data               
            else:
                total_train_data = np.concatenate((total_train_data,train_data))
        
        #X = np.array([i[0] for i in total_train_data]).reshape(-1,width,height,3)
        #experiment, change up width and height, as original array is height, width
        X = np.array([i[0] for i in total_train_data]).reshape(-1,height,width,3)
        y = [i[1][:7] for i in total_train_data]
        y = np.asarray(y)
    #    print("y is a {}".format(y.shape))

        #y = np.array(y, dtype=np.int32).reshape(1000,)
        
        X_train, X_valid, y_train, y_valid = train_test_split(X, y, random_state=0)

    #    for a in y_train:
    #        print("y is a {}".format(a))

        move, action = create_action_move(y_train)

        test_move, test_action = create_action_move(y_valid)
        #for i in range(len(move)):
    #
    #       print("I    {}".format(move[i]))
    #  return
        train_model(model_name, model_vers, 7, width, height, X_train, y_train, X_valid, y_valid, True)
        model_vers = model_vers + 1
                    
main()
