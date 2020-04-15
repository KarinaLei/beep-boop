import cv2
import time
import numpy as np

import constants

# Number of sections = 6
STEP = 3
SEC_LIM = 4000/9
# Edge sections have width of 106 px, middle sections have width of 107 px
SECS = [0, 106, 213, 320, 427, 534, 640]

def state(img, crosswalk):

    state = []

    state_sum = [sum([1 for dim in img[constants.PATH_INIT_H:constants.H:STEP, SECS[incr]:SECS[incr + 1]:STEP] 
        for pix in dim if pix > constants.BW_LIM]) for incr in range(0,6)]

    if(np.sum(state_sum[0:3]) > SEC_LIM):
        state.append(np.argmax(state_sum[0:3]))
    else:
        state.append(-1)

    if(np.sum(state_sum[3:6]) > SEC_LIM):
        state.append(2 - np.argmax(state_sum[3:6]))
    else:
        state.append(-1)

    if crosswalk[1]:
        state[0] -= 0.3
    
    return state


CORNER_LIM = 120    # was 225 before

def corner(img):

    img_sample = img[375:415:2,int(constants.CORNER_L):int(constants.CORNER_R):2]
    print("printing corner sum")
    print(sum([1 for dim in img_sample for pix in dim if pix > constants.BW_LIM]))
    return sum([1 for dim in img_sample for pix in dim if pix > constants.BW_LIM]) > CORNER_LIM
