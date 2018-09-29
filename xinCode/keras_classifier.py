#-*- coding:utf-8 -*-
# Author : 7secondsFish
# Data : 18-7-6 上午11:18
import glob

import keras
from PIL import Image
from keras import optimizers
from keras.layers import Convolution2D, MaxPooling2D, Activation, Flatten, Dense, np ,Dropout
from keras.models import Sequential
import tensorflow as tf
import os

from keras.optimizers import Adam

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#path = '/opt/flows/flower_photos/'
path = '/opt/cloths/'
batch_size = 32
def read_img(path):
    #writer = tf.python_io.TFRecordWriter("test01.tfrecords")
    cate = [path + x for x in os.listdir(path) if os.path.isdir(path + x)]
    print(cate)
    imgs = []
    labels = []
    for idx, folder in enumerate(cate):
        for im in glob.glob(folder + '/*.jpg'):
            print('reading the images:%s' % (im))
            ori_im =  Image.open(im).resize((100,100))
            img = np.array(ori_im)
            if len(img.shape) == 2:
                print("error shape")
            else:
                imgs.append(img)
                labels.append(idx)
    #writer.close()
    return np.asarray(imgs, np.float32), np.asarray(labels, np.int32)

def minibatches(inputs=None, targets=None, batch_size=None, shuffle=False):
    assert len(inputs) == len(targets)
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)
    while 1:
        for start_idx in range(0, len(inputs) - batch_size + 1, batch_size):
            if shuffle:
                excerpt = indices[start_idx:start_idx + batch_size]
            else:
                excerpt = slice(start_idx, start_idx + batch_size)
            yield (inputs[excerpt], targets[excerpt])



data, label = read_img(path)
print(data.shape)

# 打乱顺序
num_example = data.shape[0]
arr = np.arange(num_example)
np.random.shuffle(arr)
data = data[arr]
label = label[arr]

# 将所有数据分为训练集和验证集
ratio = 0.8
s = np.int(num_example * ratio)
x_train = data[:s]
y_train = label[:s]
x_val = data[s:]
y_val = label[s:]
#x = tf.placeholder(tf.float32, shape=[None, 100,100,3], name='x')
model = Sequential()
#第一个卷积层（100——>50)
model.add(Convolution2D(
    filters=32,
    kernel_size=[5, 5],
    padding="same",
    activation=tf.nn.relu,
    input_shape=(100,100,3),
    kernel_initializer=tf.truncated_normal_initializer(stddev=0.01)
))
model.add(MaxPooling2D(
    pool_size=(2,2),
    strides=(2,2),
    padding='same', #padding method
))
model.add(Dropout(0.2))
# 第二个卷积层(50->25)
model.add(Convolution2D(
    filters=64,
    kernel_size=[5, 5],
    padding="same",
    activation=tf.nn.relu,
    kernel_initializer=tf.truncated_normal_initializer(stddev=0.01)
))
model.add(MaxPooling2D(
    pool_size=(2,2),
    strides=(2,2),
    padding='same', #padding method
))
model.add(Dropout(0.2))
# 第三个卷积层(25->12)
model.add(Convolution2D(
    filters=128,
    kernel_size=[3, 3],
    padding="same",
    activation=tf.nn.relu,
    kernel_initializer=tf.truncated_normal_initializer(stddev=0.01)
))
model.add(MaxPooling2D(
    pool_size=(2,2),
    strides=(2,2),
    padding='same', #padding method
))
model.add(Dropout(0.2))
# 第四个卷积层(12->6)
model.add(Convolution2D(
    filters=256,
    kernel_size=[2, 2],
    padding="same",
    activation=tf.nn.relu,
    kernel_initializer=tf.truncated_normal_initializer(stddev=0.01)
))
model.add(MaxPooling2D(
    pool_size=(2,2),
    strides=(2,2),
    padding='same', #padding method
))
model.add(Dropout(0.2))
model.add(Flatten())
# 全连接层
model.add(Dense(1024))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.2))
model.add(Dense(3))
#//使用softmax进行分类
model.add(Activation('softmax'))


print('compile begin-------------')
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

model.fit_generator(minibatches(x_train, y_train, batch_size, shuffle=True),epochs=25,verbose=1,steps_per_epoch =50)
loss,accuracy=model.evaluate(x_val,y_val)
print('test loss: ', loss)
print('test accuracy: ', accuracy)
model.save("my_model.h5")

if __name__ == '__main__':
    pass

    