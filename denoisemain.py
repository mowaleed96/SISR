import tensorflow as tf
from  denoisemodel import denoiser

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_integer("epoch", 100000, "Number of epoch")
flags.DEFINE_integer("notGrayScale", 1, "input not gray scale")
flags.DEFINE_string("is_train", "True", "if the train")
flags.DEFINE_string("checkpoint_dir", "denoise checkpoint", "Name of checkpoint directory")
flags.DEFINE_float("learning_rate", 1e-4 , "The learning rate")
flags.DEFINE_string("result_dir", "result", "Name of result directory")
flags.DEFINE_string("path", "Training/", "path of photos")

def main(_):
    with tf.Session() as sess:
        espcn = denoiser(sess,
                      is_train = FLAGS.is_train,
                      )
        espcn.train(FLAGS)

if __name__=='__main__':
    tf.app.run() # parse the command argument , the call the main function
