import tensorflow as tf
import numpy as np


class denoiser(object):

    def __init__(self, sess, input):
        self.sess = sess
        self.build_model()

        self.train_op = tf.train.AdamOptimizer(learning_rate=0.001).minimize(self.loss)
        tf.initialize_all_variables().run()

        hello = self.sess.run([self.train_op, self.loss],
                              feed_dict={self.input: np.array(input), self.label: [0, 0, 1]})

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

    def getvalue(self, x):
        result = self.pred.eval(feed_dict={self.input: np.array(x)})
        return result
