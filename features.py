import scipy
from scipy.stats import skew
import numpy as np
def extract(img):
    """
        extract skewness and kurtosis for an image 
    """

    skew = scipy.stats.skew(img)
    kurt = scipy.stats.kurtosis(img)

    return np.sum(skew)/float(len(skew)), np.sum(kurt)/float(len(kurt))