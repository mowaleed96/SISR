import scipy
from scipy.stats import skew
import numpy as np
def extract(img):
    """
        extract skewness and kurtosis for an image 
    """
    w, h, _ = img.shape
    imgsize = w*h

    skew = scipy.stats.skew(img)
    skew = np.sum(skew)/imgsize


    kurt = scipy.stats.kurtosis(img)
    kurt = np.sum(kurt)/imgsize

    return skew, kurt