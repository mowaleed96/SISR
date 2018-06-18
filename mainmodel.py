import os
import cv2 as cv
import tensorflow as tf

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string("path", "", "path of the testing image")
flags.DEFINE_boolean("video", False, "upscalling is done to video not single image")

def sisr():
    # denoise it
    os.system(
        'python denoisemain.py --is_train=False --path=' + str(FLAGS.path))  # "/home/amr/Downloads/TensorFlow-ESPCN-master/tst/1.bmp"')

    x = FLAGS.path.split('/')
    newpath = ""

    for i in range(1, len(x) - 2):
        newpath += '/' + x[i]
    newpath += './DeNoised/'
    newpath += x[-1]

    print "here "+str(newpath)

    # SISR it
    if FLAGS.video:
        os.system('python main.py --is_train=False --result_dir=new-frames --test_img='+newpath)#"/home/amr/Downloads/TensorFlow-ESPCN-master/DeNoised/1.bmp"')
    else:
        os.system('python main.py --is_train=False --test_img=' + newpath)  # "/home/amr/Downloads/TensorFlow-ESPCN-master/DeNoised/1.bmp"')

sisr()
