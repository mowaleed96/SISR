import tensorflow as tf
from  model import denoiser

def main():
     with tf.Session() as sess:
        x=denoiser(sess,[[1],[2],[3],[4],[5],[6]])
        y=x.getvalue([[1],[2],[3],[4],[5],[6]]);
        print(y)

if __name__=='__main__':
    main() 