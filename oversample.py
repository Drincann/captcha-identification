import random
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


def basenameWithoutExt(path):
    return os.path.basename(path).split('.')[0]


def path2imgarray(path, binary=True):
    if INPUT_CHANNELS == 1:
        binary = True
    img = PIL.Image.open(path)
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img = np.array(img)

    # def binaryzation(img):
    #     cv_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #     return cv_img
    # img = binaryzation(img) if binary else img
    # img = img / 255.0
    img = img.reshape(IMG_HEIGHT, IMG_WIDTH, (1 if binary else 3))
    return img


resample = keras.Sequential([
    keras.layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, INPUT_CHANNELS)),
    keras.layers.RandomRotation(0.05),
    keras.layers.RandomZoom(0.1),
])

parser = argparse.ArgumentParser(description='captcha')
parser.add_argument('-i', '--inputdir', type=str, default=100,
                    help='inputdir')
parser.add_argument('-t', '--target', type=int,
                    required=True, help='target count')

args = parser.parse_args()
inputdir = args.inputdir
targetCount = args.target
if not os.path.exists(inputdir):
    raise Exception('inputdir not exists')

originImgList = [filename for filename in os.listdir(inputdir) if filename.endswith(
    ('.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG', '.bmp', '.BMP'))]

while len(os.listdir(inputdir)) < targetCount:
    # 随机选择一张图片
    imgList = [filename for filename in os.listdir(inputdir) if filename.endswith(
        ('.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG', '.bmp', '.BMP'))]
    filename = random.choice(imgList)

    img = path2imgarray(os.path.join(inputdir, filename)).reshape(
        (1, IMG_HEIGHT, IMG_WIDTH, INPUT_CHANNELS))
    img = np.array(resample(img))
    print(img.shape)
    cv2.imwrite(os.path.join(
        inputdir, f'{basenameWithoutExt(filename)}_resample.jpg'), img[0])

    print(
        f"{inputdir} resample {filename} to {basenameWithoutExt(filename)}_resample.jpg {len(os.listdir(inputdir))}/{targetCount}")
for filename in originImgList:
    path = os.path.join(inputdir, filename)
    img = path2imgarray(os.path.join(inputdir, filename)).reshape(
        (1, IMG_HEIGHT, IMG_WIDTH, INPUT_CHANNELS))
    img = np.array(resample(img))
    print(img.shape)
    cv2.imwrite(os.path.join(
        inputdir, f'{basenameWithoutExt(filename)}.jpg'), img[0])
    print(
        f"{inputdir} resample {filename} to {basenameWithoutExt(filename)}.jpg {len(os.listdir(inputdir))}/{targetCount}")
