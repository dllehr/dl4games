import numpy as np
import cv2
import argparse
import sys
import time
import os
import yaml

def load_cfg( config_file, game_template):
    with open(config_file, 'r') as stream:
        cfg = yaml.load(stream)
        cfg = cfg['templates'][game_template]
    return cfg

def load_dataset(ds_name, single_file=False, height=None, width=None):

    if(single_file):
        if(width == None or height == None):
            print("ERROR: You must specify height and width when using single file")
            return -1
    else:
        meta_file = '{}.meta'.format(ds_name)
        if os.path.isfile(meta_file):
            with open(meta_file, 'r') as stream:
                data_loaded = yaml.load(stream)
            height = data_loaded['height']
            width = data_loaded['width']
        else:
            print("ERROR: Loading string of input data requires a .meta file")
            return -1

    starting_value = 1

    while True:
    #file_name = 'training_data-{}.npy'.format(starting_value)
        if (single_file):
            file_name = ds_name
        else:
            file_name = '{}-{}.npy'.format(ds_name, starting_value)

        if os.path.isfile(file_name):
            print("File {} exists, loading".format(file_name))
            train_data = np.load(file_name)
            np.random.shuffle(train_data)
            if starting_value == 1:
                print('count is zero')
                total_train_data = train_data
            else:
                total_train_data = np.concatenate((total_train_data,train_data))

            starting_value += 1

            if(single_file):
                break
        else:
            print("File {} does not exists, stopping".format(file_name))
            break
            
    X = np.array([i[0] for i in total_train_data]).reshape(-1,height,width,3)
    y = np.array([i[1] for i in total_train_data])
    return X, y