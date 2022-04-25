import random
import string
from PIL import Image
import os
from PIL import ImageDraw, ImageFont
import argparse


# 生成数字验证码


def gen(text):
    captcha = Image.new('RGB', (160, 60), (255, 255, 255))
    # 字体颜色
    fontColor = (random.randint(0, 255), random.randint(
        0, 255), random.randint(0, 255))
    fontSize = random.randint(24, 30)
    font = ImageFont.truetype(
        './font.ttc', fontSize)
    draw = ImageDraw.Draw(captcha)
    for i in range(4):

        draw.text((40 * i + 10, 10),
                  text[i], font=font, fill=fontColor)
    noNoiseCaptcha = captcha.copy()
    # 干扰线
    for i in range(random.randint(5, 10)):
        lineColor = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        x1 = random.randint(0, 160)
        y1 = random.randint(0, 60)
        x2 = random.randint(0, 160)
        y2 = random.randint(0, 60)
        draw.line([(x1, y1), (x2, y2)], fill=lineColor)
    # 干扰点
    for i in range(random.randint(100, 200)):
        pointColor = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        draw.point([random.randint(0, 160), random.randint(0, 60)],
                   fill=pointColor)
    return captcha, noNoiseCaptcha


parser = argparse.ArgumentParser(description='captcha')
parser.add_argument('-o', '--outdir', type=str,
                    default='./dataset', help='output dir')
parser.add_argument('-n', '--num', type=int, default=100,
                    help='number of captchas')
args = parser.parse_args()
outdir = args.outdir
num = args.num

noisePath = os.path.join(outdir, 'noise')
noNoisePath = os.path.join(outdir, 'noNoise')
if not os.path.exists(noisePath):
    os.makedirs(noisePath)

if not os.path.exists(noNoisePath):
    os.makedirs(noNoisePath)

textSet = set()
while len(textSet) < num:
    text = ''.join([random.choice(string.ascii_uppercase) for i in range(4)])
    if text not in textSet:
        textSet.add(text)
        noise, noNoise = gen(text)
        noise.save(os.path.join(noisePath, text + '.jpg'))
        noNoise.save(os.path.join(noNoisePath, text + '.jpg'))
