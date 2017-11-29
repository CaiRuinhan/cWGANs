'''

Script to create a nxm matrix of photos generated by the generator

'''

import cv2
import tensorflow as tf
import numpy as np
import sys
sys.path.insert(0, '../ops/')

from tf_ops import *
import data_ops
from nets import *

if __name__ == '__main__':

   checkpoint_dir = sys.argv[1]

   n = 15 # cols
   m = 5  # rows

   num_images = n*m

   img_size = (64, 64, 3)

   canvas = 255*np.ones((m*img_size[0]+(10*m)+10, n*img_size[1]+(10*n)+10, 3), dtype=np.uint8)
   
   z = tf.placeholder(tf.float32, shape=(num_images, 100), name='z')
   y = np.random.choice([0, 1], size=(num_images, 9))
   generated_images = netG(z, y, num_images)
   
   init = tf.global_variables_initializer()
   sess = tf.Session()
   sess.run(init)
   
   saver = tf.train.Saver()
   ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
   if ckpt and ckpt.model_checkpoint_path:
      print "Restoring previous model..."
      try:
         saver.restore(sess, ckpt.model_checkpoint_path)
         print "Model restored"
      except:
         raise
         print "Could not restore model"
         exit()

   batch_z = np.random.normal(-1.0, 1.0, size=[num_images, 100]).astype(np.float32)
   gen_imgs = sess.run([generated_images], feed_dict={z:batch_z})
   gen_imgs = np.squeeze(np.asarray(gen_imgs))

   start_x = 10
   start_y = 10

   x = 0
   y = 0

   for img in gen_imgs:
      img = (img+1.)/2. # these two lines properly scale from [-1, 1] to [0, 255]
      img *= 255.0/img.max()

      end_x = start_x+64
      end_y = start_y+64
      
      canvas[start_y:end_y, start_x:end_x, :] = img

      if x < n:
         start_x += 64+10
         x += 1
      if x == n:
         x       = 0
         start_x = 10
         start_y = end_y + 10
         end_y   = start_y+64

   import scipy.misc as misc
   misc.imsave('results.png', canvas)
   #cv2.imwrite('results.jpg', canvas)
   #cv2.imshow('canvas', canvas)
   #cv2.waitKey(0)
   #cv2.destroyAllWindows()
