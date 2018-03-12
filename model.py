import tensorflow as tf
import numpy as np
from reader import  *
import cv2
from filters import *
from features import *
import time

class denoiser(object):

    def __init__(self,
                 sess,
                 is_train,
                 batch_size,
                 test_img,
                 ):

        self.sess = sess
        self.is_train = is_train
        self.batch_size = batch_size
        self.test_img = test_img
        self.build_model()

    """def __init__(self, sess, input):
        self.sess = sess
        self.build_model()

        self.train_op = tf.train.AdamOptimizer(learning_rate=0.001).minimize(self.loss)
        tf.initialize_all_variables().run()

        hello = self.sess.run([self.train_op, self.loss],
                              feed_dict={self.input: np.array(input), self.label: [0, 0, 1]})
    
        def getvalue(self, x):
            result = self.pred.eval(feed_dict={self.input: np.array(x)})
            return result
    """
    def build_model(self):
        self.input = tf.placeholder(tf.float32, shape=(6, 1), name='input')
        self.label = tf.placeholder(tf.float32, shape=(3), name='Label')
        self.w = tf.Variable(tf.random_normal([6, 6], stddev=np.sqrt(2.0 / 6 * 6 / 3)), name='w')
        self.pred = self.model()
        return self.output

    def model(self):
        pattern = tf.transpose(tf.matmul(self.input, self.w, True))
        sums = [
            pattern[0] + pattern[1],
            pattern[2] + pattern[3],
            pattern[4] + pattern[5],
        ]
        self.output = tf.sigmoid(sums)
        self.loss = tf.reduce_mean(tf.square(self.label[0] - self.output[0]) +
                                   tf.square(self.label[1] - self.output[1]) +
                                   tf.square(self.label[2] - self.output[2]))

        tmp_sum = tf.summary.merge_all()
        tmp_sum_wrt = tf.summary.FileWriter("logs", self.sess.graph)
        return self.output

    def train(self,config ):
        images,labels=load_dir(config.path);
        if(config.isGrayScale!="True" and config.isGrayScale!="true"):
            for i in range(0,len(images)) :
                images[i]=cv2.cvtColor( images[i], cv2.COLOR_RGB2GRAY )

        list_features= self.get_features(images)

        self.train_op = tf.train.AdamOptimizer(learning_rate=0.001).minimize(self.loss)
        tf.initialize_all_variables().run()
        time_ = time.time()
        counter=0
        for ep in range(0,config.epoch):
            for i in range(0,len(list_features)):
                _, err = self.sess.run([self.train_op, self.loss],
                              feed_dict={self.input: np.array(list_features[i]), self.label:labels[i]})
                counter+=1
            if counter % 10 == 0:
                print("Epoch: [%2d], step: [%2d], time: [%4.4f], loss: [%.8f]" % ((ep + 1), counter , time.time() - time_, err))
                # print(label_[1] - self.pred.eval({self.images: input_})[1],'loss:]',err)
            if counter % 500 == 0:
                self.save(config.checkpoint_dir, counter)

    def get_features(self, images):
        list_features = []
        for image in images:
            Ywiener=wiener(image)
            Ymedian=median(image)
            #Yhomomorphic=homomorphic(image)
            Wwiener=np.subtract(image,Ywiener)
            Wmedian = np.subtract(image, Ymedian)
            #Whomomorphic = np.subtract(image, Yhomomorphic)
            features=[]
            features.append(extract(Wwiener))
            features.append(extract(Wmedian))
            #features.append(extract(Whomomorphic))
            list_features.append(features)

        return  list_features