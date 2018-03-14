import scipy
from scipy.stats import skew
import numpy as np
def extract(img):
    """
        extract skewness and kurtosis for an image 
    """
    shape = img.shape
    imgsize = shape[0]*shape[1] # width * hieght

    skew = scipy.stats.skew(img)
    skew = np.sum(skew)/imgsize

    kurt = scipy.stats.kurtosis(img)
    kurt = np.sum(kurt)/imgsize
    
    return skew, kurt