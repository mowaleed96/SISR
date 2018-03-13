import tensorflow as tf
import numpy as np
from reader import *
import cv2
from filters import *
from features import *
import time


class denoiser(object):

    def __init__(self,
                 sess,
                 is_train,
                 ):
        self.sess = sess
        self.is_train = is_train
        self.build_model()

    def build_model(self):
        self.input = tf.placeholder(tf.float32, shape=(4, 1), name='input')
        self.label = tf.placeholder(tf.float32, shape=(3), name='Label')
        self.w = tf.Variable(tf.random_normal([4, 6], stddev=np.sqrt(2.0 / 4 * 6 / 3)), name='w')
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

        self.saver = tf.train.Saver()  # To save checkpoint

        tmp_sum = tf.summary.merge_all()
        tmp_sum_wrt = tf.summary.FileWriter("logs", self.sess.graph)
        return self.output

    def train(self, config):
        images, labels = load_dir(config.path)
        if (config.isGrayScale != "True" and config.isGrayScale != "true"):
            for i in range(0, len(images)):
                images[i] = cv2.cvtColor(images[i], cv2.COLOR_RGB2GRAY)
        print("--finished loading data")
        list_features = self.get_features(images)
        print("----got features")
        self.train_op = tf.train.AdamOptimizer(learning_rate=config.learning_rate).minimize(self.loss)
        tf.initialize_all_variables().run()
        time_ = time.time()
        counter = 0
        self.load(config.checkpoint_dir)

        if config.is_train=="True":
            print("starting training")
            for ep in range(0, config.epoch):
                for i in range(0, len(list_features)):
                    #print(list_features[i])
                    #print(i)
                    inputlabel=[]
                    for j in range(0,3):
                        if i == labels[i]:
                            inputlabel.append(1)
                        else:
                            inputlabel.append(0)

                    _, err = self.sess.run([self.train_op, self.loss],
                                           feed_dict={self.input: np.array(list_features[i]),
                                                      self.label: np.array(inputlabel)})
                    counter += 1
                if counter % 10 == 0:
                    print("Epoch: [%2d], step: [%2d], time: [%4.4f], loss: [%.8f]" % (
                    (ep + 1), counter, time.time() - time_, err))
                    # print(label_[1] - self.pred.eval({self.images: input_})[1],'loss:]',err)
                if counter % 500 == 0:
                    self.save(config.checkpoint_dir, counter)
        else:
            accuracy=0
            for i in range(0,len(list_features)):
                results = self.pred.eval({self.input: np.array(list_features[i])})
                maxx=0
                index=0
                for j in range(0,len(results)):
                    if(results[j]>maxx):
                        maxx=results[j]
                        index=j
                print("input = {} and result = {}".format(labels[i],index))
                if index==labels[i]:
                    accuracy+=1
            print("Accuracy = {}".format(accuracy/float(len(list_features))))

    def get_features(self, images):
        print("---get features")
        list_features = []
        for image in images:
            Ywiener = wiener(image)
            Ymedian = median(image)
            # Yhomomorphic=homomorphic(image)
            Wwiener = np.subtract(image, Ywiener)
            Wmedian = np.subtract(image, Ymedian)
            # Whomomorphic = np.subtract(image, Yhomomorphic)
            features = []

            skew1,kurt1=extract(Wwiener)
            features.append([skew1])
            features.append([kurt1])

            skew2, kurt2=extract(Wmedian)
            features.append([skew2])
            features.append([kurt2])

            """
            skew3, kurt3=extract(Whomomorphic)
            features.append([skew3])
            features.append([kurt3])
            """

            list_features.append(features)

        return list_features

    def save(self, checkpoint_dir, step):
        """
            To save the checkpoint use to test or pretrain
        """
        model_name = "noise-preprocess.model"
        checkpoint_dir = os.path.join(checkpoint_dir, "train")

        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)

        self.saver.save(self.sess,
                        os.path.join(checkpoint_dir, model_name),
                        global_step=step)

    def load(self, checkpoint_dir):
        """
            To load the checkpoint use to test or pretrain
        """
        print("\nReading Checkpoints.....\n\n")
        checkpoint_dir = os.path.join(checkpoint_dir, "train")
        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)

        # Check the checkpoint is exist
        if ckpt and ckpt.model_checkpoint_path:
            ckpt_path = str(ckpt.model_checkpoint_path)  # convert the unicode to string
            self.saver.restore(self.sess, os.path.join(os.getcwd(), ckpt_path))
            print("\n Checkpoint Loading Success! %s\n\n" % ckpt_path)
        else:
            print("\n! Checkpoint Loading Failed \n\n")
