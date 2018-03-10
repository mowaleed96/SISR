import scipy 


def median(img,Ksize=None):
    med_img = scipy.signal.medfilt2d(img,Ksize)
    return med_img

def wiener(img,Ksize=None):
    win_img = scipy.signal.wiener(img,Ksize)
    return win_img

def homomorphic(img):
    return None