import tensorflow as tf
from  model import denoiser

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_integer("epoch", 2000, "Number of epoch")
flags.DEFINE_integer("isGrayScale", 1, "is input gray scale or no")
flags.DEFINE_boolean("is_train", "True", "if the train")
flags.DEFINE_string("checkpoint_dir", "checkpoint", "Name of checkpoint directory")
flags.DEFINE_float("learning_rate", 1e-5 , "The learning rate")
flags.DEFINE_integer("batch_size", 128, "the size of batch")
flags.DEFINE_string("result_dir", "result", "Name of result directory")
flags.DEFINE_string("path", "Training/", "path of photos")

def main(_): #?
    with tf.Session() as sess:
        espcn = denoiser(sess,
                      is_train = FLAGS.is_train,
                      batch_size = FLAGS.batch_size,
                      test_img = FLAGS.test_img,
                      )
        espcn.train(FLAGS)

if __name__=='__main__':
    tf.app.run() # parse the command argument , the call the main function
