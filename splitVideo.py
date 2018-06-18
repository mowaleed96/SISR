
import cv2
import numpy as np
import os

# Playing video from file:
def split():
    cap = cv2.VideoCapture('test.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    print (str(fps))
    try:
        if not os.path.exists('old-frames'):
            os.makedirs('old-frames')
    except OSError:
        print ('Error: Creating directory of data')
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for currentFrame in range(0,length):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Saves image of the current frame in jpg file
        name = './old-frames/' + str(currentFrame) + '.jpg'
        print ('Creating...' + name)
        cv2.imwrite(name, frame)

        # To stop duplicate images
        currentFrame += 1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return fps

if __name__=='__main__':
    split()