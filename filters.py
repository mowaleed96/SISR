import scipy
import numpy as np
from scipy.signal import medfilt2d
import cv2


def medianf(img, Ksize=7):
    med_img = scipy.signal.medfilt2d(img, Ksize)
    return med_img


def wienerf(img, Ksize=8):
    win_img = scipy.signal.wiener(img, Ksize, 20)
    return win_img


def homomorphicf_RGB(img):
    img_YUV = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    print img_YUV.shape

    y = img_YUV[:, :, 0]

    rows = y.shape[0]
    cols = y.shape[1]

    imgLog = np.log1p(np.array(y, dtype='float') / 255)

    M = 2 * rows + 1
    N = 2 * cols + 1

    sigma = 10
    (X, Y) = np.meshgrid(np.linspace(0, N - 1, N), np.linspace(0, M - 1, M))
    Xc = np.ceil(N / 2)
    Yc = np.ceil(M / 2)
    gaussianNumerator = (X - Xc) ** 2 + (Y - Yc) ** 2

    LPF = np.exp(-gaussianNumerator / (2 * sigma * sigma))
    HPF = 1 - LPF

    LPF_shift = np.fft.ifftshift(LPF.copy())
    HPF_shift = np.fft.ifftshift(HPF.copy())

    img_FFT = np.fft.fft2(imgLog.copy(), (M, N))
    img_LF = np.real(np.fft.ifft2(img_FFT.copy() * LPF_shift, (M, N)))
    img_HF = np.real(np.fft.ifft2(img_FFT.copy() * HPF_shift, (M, N)))

    gamma1 = 0.3
    gamma2 = 1.5
    img_adjusting = gamma1 * img_LF[0:rows, 0:cols] + gamma2 * img_HF[0:rows, 0:cols]

    img_exp = np.expm1(img_adjusting)  # exp(x) + 1
    img_exp = (img_exp - np.min(img_exp)) / (np.max(img_exp) - np.min(img_exp))
    img_out = np.array(255 * img_exp, dtype='uint8')

    img_YUV[:, :, 0] = img_out
    result = cv2.cvtColor(img_YUV, cv2.COLOR_YUV2BGR)
    return result


def homomorphicf(img):
    # ref code can be found here
    # : https://stackoverflow.com/questions/24731810/segmenting-license-plate-characters
    # Number of rows and columns
    rows = img.shape[0]
    cols = img.shape[1]

    # Convert image to 0 to 1, then do log(1 + I)
    imgLog = np.log1p(np.array(img, dtype="float") / 255)

    # Create Gaussian mask of sigma = 10
    M = 2 * rows + 1
    N = 2 * cols + 1
    sigma = 10
    (X, Y) = np.meshgrid(np.linspace(0, N - 1, N), np.linspace(0, M - 1, M))
    centerX = np.ceil(N / 2)
    centerY = np.ceil(M / 2)
    gaussianNumerator = (X - centerX) ** 2 + (Y - centerY) ** 2

    # Low pass and high pass filters
    Hlow = np.exp(-gaussianNumerator / (2 * sigma * sigma))
    Hhigh = 1 - Hlow

    # Move origin of filters so that it's at the top left corner to
    # match with the input image
    HlowShift = scipy.fftpack.ifftshift(Hlow.copy())
    HhighShift = scipy.fftpack.ifftshift(Hhigh.copy())

    # Filter the image and crop
    If = scipy.fftpack.fft2(imgLog.copy(), (M, N))
    Ioutlow = scipy.real(scipy.fftpack.ifft2(If.copy() * HlowShift, (M, N)))
    Iouthigh = scipy.real(scipy.fftpack.ifft2(If.copy() * HhighShift, (M, N)))

    # Set scaling factors and add
    gamma1 = 0.3
    gamma2 = 1.5
    Iout = gamma1 * Ioutlow[0:rows, 0:cols] + gamma2 * Iouthigh[0:rows, 0:cols]

    # Anti-log then rescale to [0,1]
    Ihmf = np.expm1(Iout)
    Ihmf = (Ihmf - np.min(Ihmf)) / (np.max(Ihmf) - np.min(Ihmf))
    Ihmf = np.array(255 * Ihmf, dtype="uint8")
    return Ihmf
