import cv2
import os, os.path
import numpy as np
import cv2
import scipy.misc

def load_dir(dir_path = "images/"):
    """
        load all images from directory
    """
    print("-loading images from %s"%(dir_path))
    image_path_list = []
    valid_image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]
    image_list = []
    label_list = []
    if dir_path.endswith('.bmp') or dir_path.endswith('.jpg'):
        label_list.append(0)
        image_path_list.append(dir_path)
    else:
        for file in os.listdir(dir_path):
            extension = os.path.splitext(file)[1]
            if extension.lower() not in valid_image_extensions:
                continue
            label_list.append(int(file[0]))
            image_path_list.append(os.path.join(dir_path, file))

    for imagePath in image_path_list:
        image = cv2.imread(imagePath)
        if image is None:
            print ("Error loading: " + imagePath)
        else:
            image_list.append(image)

    return image_list,label_list,image_path_list


def load_img(img_path = "images/"):
    """
        load one image
    """
    image = cv2.imread(img_path)
    return image


def write_img(img,path,ok,filterapply):

    x = path.split('/')
    realpath="/";

    for i in range(1,len(x)-2):
        realpath+=x[i]+"/"
    realpath+="DeNoised"

    print "here is ok "+str(ok)

    if ok!=1 :
        print "noise type is "+str(filterapply)
        realpath=realpath+"/"+x[-1]
        print filterapply
        cv2.imshow('ezay', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    	cv2.imwrite(realpath,img)
