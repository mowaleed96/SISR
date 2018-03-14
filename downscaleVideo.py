import os
import scipy.misc
import cv2

from utils import (
    checkimage,
    preprocess
)


def down():
    images = []
    input_dir = './old frames/'
    output_dir = './downscaled frames/'
    cnt = 1
    for subdir, dirs, files in os.walk(input_dir):
        for file in files:
            y = os.path.join(subdir, file)
            print(y)
            if (y.endswith('jpg') == 0 and y.endswith('png') == 0):
                continue
            x,_ = preprocess(y, 3)
            #checkimage(x)
            z = os.path.join(output_dir, file)
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)
            cv2.imwrite(z, x)
            cnt += 1
