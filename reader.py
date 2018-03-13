import cv2
import os, os.path

# reference: https://scottontechnology.com/open-multiple-images-opencv-python/


def load_dir(dir_path = "images/"): 
    """
        load all images from directory
    """
    print("-load data")
    image_path_list = []
    valid_image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]
    image_list = []
    label_list = []
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
    
    return image_list,label_list


def load_img(img_path = "images/"):
    """
        load one image
    """
    image = cv2.imread(img_path)
    return image