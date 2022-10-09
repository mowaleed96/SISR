import tensorflow as tf
from reader import *
import cv2
from filters import *
from features import *
import time
import copy



class denoiser(object):

    def __init__(self,
                 sess,
                 is_train,
                 ):
        self.sess = sess
        self.is_train = is_train
        self.build_model()

    def build_model(self):
        self.input = tf.placeholder(tf.float32, shape=(7, 1), name='input')
        self.label = tf.placeholder(tf.float32, shape=(5), name='Label')
        self.w = tf.Variable(tf.random_normal([7, 10], stddev=np.sqrt(2.0 / 7.0 * 10.0 / 3.0)), name='w')
        self.pred = self.model()
        return self.output

    def model(self):
        pattern = tf.transpose(tf.matmul(self.input, self.w, True))
        sums = [
            pattern[0] + pattern[1],
            pattern[2] + pattern[3],
            pattern[4] + pattern[5],
            pattern[6] + pattern[7],
            pattern[8] + pattern[9]
        ]
        self.output = tf.sigmoid(sums)
        self.loss = tf.reduce_mean([tf.square(self.label[0] - self.output[0]),
                                    tf.square(self.label[1] - self.output[1]),
                                    tf.square(self.label[2] - self.output[2]),
                                    tf.square(self.label[3] - self.output[3]),
                                    tf.square(self.label[4] - self.output[4])])

        self.saver = tf.train.Saver()  # To save checkpoint

        _ = tf.summary.merge_all()
        _ = tf.summary.FileWriter("logs", self.sess.graph)
        return self.output

    def train(self, config):

        print ("loading images from %s..." % (config.path))
        images, labels, _NameImage = load_dir(config.path)
        coloredImages=copy.deepcopy(images)
        if (config.notGrayScale == 1):
            print ("converting to gray scale...")
            for i in range(0, len(images)):
                images[i] = cv2.cvtColor(images[i], cv2.COLOR_RGB2GRAY)

        print("extracting features...")
        list_features = self.get_features(images)

        self.train_op = tf.train.AdamOptimizer(learning_rate=config.learning_rate).minimize(self.loss)
        tf.initialize_all_variables().run()
        time_ = time.time()
        counter = 0
        self.load(config.checkpoint_dir)

        if config.is_train == "True":
            print("starting training...")
            for ep in range(0, config.epoch):
                for i in range(0, len(list_features)):
                    # print(list_features[i])
                    # print(i)
                    inputlabel = []
                    for j in range(0, 5):
                        inputlabel.append(int(j == labels[i]))

                    _, err = self.sess.run([self.train_op, self.loss],
                                           feed_dict={self.input: np.array(list_features[i]),
                                                      self.label: np.array(inputlabel)})
                    counter += 1
                    if counter % 10 == 0:
                        print("Epoch: [%2d], step: [%2d], time: [%4.4f], loss: [%.8f]" % (
                            (ep + 1), counter, time.time() - time_, err))

                    if counter % 500 == 0:
                        print("save Check point")
                        self.save(config.checkpoint_dir, counter)
        else:
            accuracy = 0
            forEachClass=[0,0,0,0,0]
            totalEachClass=[0,0,0,0,0]
            for i in range(0, len(list_features)):
                results = self.pred.eval({self.input: np.array(list_features[i])})
                maxx = 0
                index = 0
                for j in range(0, len(results)):
                    if (results[j] > maxx):
                        maxx = results[j]
                        index = j

                if(labels[i]==index):
                    forEachClass[index]+=1

                totalEachClass[labels[i]]+=1
                self.applyFilterAndSaveImage(index, images[i], _NameImage[i])
                print("input = {} and result = {}".format(labels[i], index))
                if index == labels[i]:
                    accuracy += 1

            print("Correct For Each Class ={} \n and expact total for each class = {}".format(forEachClass,totalEachClass))
            print("Accuracy = {}".format(accuracy / float(len(list_features))))

    def get_features(self, images):

        list_features = []
        cnt = 1
        for image in images:
            image = np.float32(image)
            print "img-%d" % cnt
            cnt = cnt + 1
            print ("\tappling wiener filter")
            Ywiener = wienerf(image)
            print ("\tappling median filter")
            Ymedian = medianf(image)
            print ("\tappling homomorphic filter")
            Yhomomorphic = homomorphicf(image)
            print "\n...\n...\n..."
            Wwiener = np.subtract(image, Ywiener)
            Wmedian = np.subtract(image, Ymedian)
            Whomomorphic = np.subtract(image, Yhomomorphic)

            print "\n...\n"

            skew1, kurt1 = extract(Wwiener)

            skew2, kurt2 = extract(Wmedian)

            skew3, kurt3 = extract(Whomomorphic)

            list_features.append([[1], [skew1], [kurt1], [skew2], [kurt2], [skew3], [kurt3]])

        return list_features


    def applyFilterAndSaveImage(self,label,image,name):
        write_img(image,name,1,str(label));
        if label==0 :
            output = medianf(image)
        elif label==1 or label == 3:
            output = wienerf(image)
        elif label == 2:
            output = homomorphicf(image)
        else:
            output=image

        write_img(output,name,0,str(label));



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
            print("\n!*Checkpoint Loading Failed*!\n\n")
