import splitVideo
import makeVideo
import os
import downscaleVideo
import cv2
from functools import cmp_to_key
from PSNR import PSnr
import time

def clear():


    folder = './old-frames'
    if os.path.isdir(folder):
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)


    folder = './new-frames'
    if os.path.isdir(folder):
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    folder = './downscaled-frames'
    if os.path.isdir(folder):
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                    print(e)

def isnum(num):
    try:
        int(num)
        return True
    except:
        return False

def image_sort(x, y):
    x = int(x.split(".")[0])
    y = int(y.split(".")[0])
    return x - y

def upscale():
    timebefor = time.time();

    fps = splitVideo.split()

    print("fps is " + str(fps))
    timeafter = time.time();
    file = open("time1.txt", "w")
    file.write(str(timeafter - timebefor) + " after spliting \n")
    file.close()

    #
    #downscaleVideo.down()



#send the files to the model
    dir_path = './old-frames'



    images = []
    for f in os.listdir(dir_path):
        if f.endswith('jpg'):
            images.append(f)

    int_name = images[0].split(".")[0]
    if isnum(int_name):
        images = sorted(images, key=cmp_to_key(image_sort))
    else:
        print("Failed to sort numerically, switching to alphabetic sort")
        images.sort()

    cnt=0

    timebefor = time.time();
    tot_psnr=0
    for f in images:
        flag = "--video=True --path=./old-frames/"
        flag = flag + f
        os.system('python mainmodel.py '+flag)
        os.rename('new-frames/result.png', 'new-frames/'+str(cnt)+'.png')
        tot_psnr += PSnr('old-frames/', 'new-frames', str(cnt)+'.jpg', str(cnt)+'.png')
        cnt = cnt+1
    tot_psnr/=len(images)
    timeafter = time.time();
    file = open("time2.txt", "w")
    file.write(str(timeafter - timebefor) + " after upscalling \n")
    file.close()

    timebefor = time.time();
    makeVideo.make(fps)
    timeafter = time.time();
    file = open("time3.txt", "w")
    file.write(str(timeafter - timebefor) + " after making video \n")
    file.close()

    file = open("avg_psnr.txt", "w")
    file.write(str(tot_psnr) + " average PSNR\n")
    file.close()


if  __name__  ==  '__main__':
    clear()
    upscale()
