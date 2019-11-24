import time

keyList = []
for char in "abcdefghijklmnopqrstuvwxyz 123456789,.'£$/\\":
    keyList.append(char)

def key_check(kl):
    keys = []
    for key in keyList:
        if kl.is_pressed(key):
            keys.append(key)
    return keys