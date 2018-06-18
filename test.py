import cv2
import numpy as np
import scipy
from scipy.signal import medfilt2d


def imshow(img):
    cv2.imshow('', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def wienerf(img, Ksize=8):
    win_img = scipy.signal.wiener(img, Ksize, 1100)
    return win_img


img = cv2.imread('./Test/3.jpg')

tr, tg, tb = cv2.split(img)
output_r = wienerf(tr)
output_g = wienerf(tg)
output_b = wienerf(tb)
result = cv2.merge((output_r, output_g, output_b))

cv2.imwrite('tst.jpg', result)
