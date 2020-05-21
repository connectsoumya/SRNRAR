import tensorflow as tf
import tensorlayer as tl
from tensorlayer.layers import *
import time


def vgg19_simple_api(rgb, reuse):
    """
    Build the VGG 19 Model
    Parameters
    -----------
    rgb : rgb image placeholder [batch, height, width, 3] values scaled [0, 1]
    """
    VGG_MEAN = [103.939, 116.779, 123.68]
    tl.layers.set_name_reuse(reuse)
    with tf.variable_scope("VGG19", reuse=reuse) as vs:
        rgb_scaled = tf.multiply(rgb, 255.0)
        # Convert RGB to BGR
        if tf.shape(rgb)[-1] == 3:
            if tf.__version__ <= '0.11':
                red, green, blue = tf.split(3, 3, rgb_scaled)
            else:  # TF 1.0
                # print(rgb_scaled)
                red, green, blue = tf.split(rgb_scaled, 3, 3)
            # assert red.get_shape().as_list()[1:] == [224, 224, 1]
            # assert green.get_shape().as_list()[1:] == [224, 224, 1]
            # assert blue.get_shape().as_list()[1:] == [224, 224, 1]
            if tf.__version__ <= '0.11':
                bgr = tf.concat(3, [
                    tf.subtract(blue, VGG_MEAN[0]),
                    tf.subtract(green, VGG_MEAN[1]),
                    tf.subtract(red, VGG_MEAN[2]),
                ])
            else:
                bgr = tf.concat(
                    [
                        tf.subtract(blue, VGG_MEAN[0]),
                        tf.subtract(green, VGG_MEAN[1]),
                        tf.subtract(red, VGG_MEAN[2]),
                    ], axis=3)
        else:
            bgr = tf.concat(
                    [
                        rgb_scaled,
                        rgb_scaled,
                        rgb_scaled,
                    ], axis=3)
        # assert bgr.get_shape().as_list()[1:] == [224, 224, 3]
        """ input layer """
        net_in = InputLayer(bgr, name='input')
        """ conv1 """
        network = Conv2d(net_in, n_filter=64, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv1_1')
        network = Conv2d(network, n_filter=64, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv1_2')
        conv_1 = network
        network = MaxPool2d(network, filter_size=(2, 2), strides=(2, 2), padding='SAME', name='pool1')
        """ conv2 """
        network = Conv2d(network, n_filter=128, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv2_1')
        network = Conv2d(network, n_filter=128, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv2_2')
        conv_2 = network
        network = MaxPool2d(network, filter_size=(2, 2), strides=(2, 2), padding='SAME', name='pool2')
        """ conv3 """
        network = Conv2d(network, n_filter=256, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv3_1')
        network = Conv2d(network, n_filter=256, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv3_2')
        network = Conv2d(network, n_filter=256, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv3_3')
        network = Conv2d(network, n_filter=256, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv3_4')
        conv_3 = network
        network = MaxPool2d(network, filter_size=(2, 2), strides=(2, 2), padding='SAME', name='pool3')
        """ conv4 """
        network = Conv2d(network, n_filter=512, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv4_1')
        network = Conv2d(network, n_filter=512, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv4_2')
        network = Conv2d(network, n_filter=512, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv4_3')
        network = Conv2d(network, n_filter=512, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv4_4')
        conv_4 = network
        network = MaxPool2d(network, filter_size=(2, 2), strides=(2, 2), padding='SAME',
                            name='pool4')  # (batch_size, 14, 14, 512)

        """ conv5 """
        network = Conv2d(network, n_filter=512, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv5_1')
        network = Conv2d(network, n_filter=512, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv5_2')
        network = Conv2d(network, n_filter=512, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv5_3')
        network = Conv2d(network, n_filter=512, filter_size=(3, 3), strides=(1, 1), act=tf.nn.relu, padding='SAME',
                         name='conv5_4')
        conv_5 = network
        # network = MaxPool2d(network, filter_size=(2, 2), strides=(2, 2), padding='SAME',
        #                     name='pool5')  # (batch_size, 7, 7, 512)
        # """ fc 6~8 """
        # network = FlattenLayer(network, name='flatten')
        # network = DenseLayer(network, n_units=4096, act=tf.nn.relu, name='fc6')
        # network = DenseLayer(network, n_units=4096, act=tf.nn.relu, name='fc7')
        # network = DenseLayer(network, n_units=1000, act=tf.identity, name='fc8')
        # print("build model finished: %fs" % (time.time() - start_time))
        return network, [conv_1, conv_2, conv_3, conv_4, conv_5]
