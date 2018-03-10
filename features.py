import scipy

def extract(img):
    """
        extract skewness and kurtosis for an image 
    """

    skew = scipy.stats.skew(img)
    kurt = scipy.stats.kurtosis(img)

    return skew, kurt