import cv2
import os
import argparse
import tensorflow as tf
from tensorflow import keras
import numpy as np
import PIL

IMG_HEIGHT = 128
IMG_WIDTH = 128
INPUT_CHANNELS = 1


def path2img(path):
    img = PIL.Image.open(path)
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    return img


def path2imgarray(path, binary=True):
    if INPUT_CHANNELS == 1:
        binary = True
    img = PIL.Image.open(path)
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img = np.array(img)

    def binaryzation(img):
        cv_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return cv_img
    img = binaryzation(img) if binary else img
    img = img / 255.0
    img = img.reshape(IMG_HEIGHT, IMG_WIDTH, (1 if binary else 3))
    return img


class AutoEncoder(keras.Model):
    def __init__(self):
        layers = keras.layers
        super().__init__()

        self.encoder = tf.keras.Sequential([
            layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, INPUT_CHANNELS)),
            layers.Conv2D(16, (3, 3), activation='relu',
                          padding='same', strides=2),
            layers.Conv2D(8, (3, 3), activation='relu',
                          padding='same', strides=2),
        ])

        self.decoder = tf.keras.Sequential([
            layers.Conv2DTranspose(
                8, kernel_size=3, strides=2, activation='relu', padding='same'),
            layers.Conv2DTranspose(
                16, kernel_size=3, strides=2, activation='relu', padding='same'),
            layers.Conv2D(1, kernel_size=(3, 3),
                          activation='sigmoid', padding='same')
        ])

    def call(self, x):
        return self.decoder(self.encoder(x))

    def encode(self, x):
        return self.encoder(x)

    def decode(self, x):
        return self.decoder(x)


parser = argparse.ArgumentParser(description='captcha')
parser.add_argument('-o', '--outdir', type=str,
                    default='./dataset', help='output dir')
parser.add_argument('-i', '--inputdir', type=str, default=100,
                    help='inputdir')
parser.add_argument('-m', '--model', type=str, required=True,)
args = parser.parse_args()
outdir = args.outdir
inputdir = args.inputdir
modelSaved = args.model
model = AutoEncoder()
model.build(input_shape=(None, IMG_HEIGHT, IMG_WIDTH, INPUT_CHANNELS))
# print(model.summary())
# exit()
model.load_weights(modelSaved)
if not os.path.exists(inputdir):
    raise Exception('inputdir not exists')

if not os.path.exists(outdir):
    os.makedirs(outdir)

jpglist = os.listdir(inputdir)
for jpg in jpglist:
    img = path2imgarray(os.path.join(inputdir, jpg))
    img = img.reshape(1, IMG_HEIGHT, IMG_WIDTH, INPUT_CHANNELS)
    img = model(img)
    img = (np.array(img)*255).astype(np.uint8)
    cv2.imwrite(os.path.join(outdir, jpg), img[0])
    # print(os.path.join(outdir, jpg))
    # exit()
