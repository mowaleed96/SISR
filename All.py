import splitVideo
import makeVideo
import os
import downscaleVideo
from functools import cmp_to_key

def clear():
    folder = './old frames'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    folder = './new frames'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    folder = './downscaled frames'
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

    fps = splitVideo.split()

    print(str(fps))

    downscaleVideo.down()



#send the files to the model
    dir_path = './downscaled frames'



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
    for f in images:
        flag = ' --test_img downscaled\ frames/'
        flag = flag + f
        os.system('python main.py --is_train=False '+flag)
        os.rename('new frames/result.png', 'new frames/'+str(cnt)+'.png')
        cnt=cnt+1
    makeVideo.make(fps)

if  __name__  ==  '__main__':
    clear()
    upscale()
