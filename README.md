# Captcha—Identification

这是一个基于卷积神经网络的验证码识别解决方案。

## dataset

使用 `./captchaGen.py` 来生成加噪以及对应去噪的验证码图片。

它被实现为一个命令行工具，你可以通过 `python ./captchaGen.py -h` 来查看支持的参数。

作为例子，我们可以通过执行下面的命令来生成训练集和验证集：

```sh
python ./captchagen.py -o ./dataset/train -n 600
python ./captchagen.py -o ./dataset/test -n 100
```

> 该工具依赖于其目录下的 `font.ttc` 文件作为验证码字体。

这些数据用来训练去噪网络（自编码器）。

训练结束后，我们需要使用 `./deNoise.py` 来生成下一阶段，训练识别网络的数据集。

它同样被实现为一个命令行工具。

作为例子，请看下面的命令：

```sh
python ./deNoise.py -i ./dataset/train/noise -o ./dataset1/train -m ./model.h5

python ./deNoise.py -i ./dataset/test/noise -o ./dataset1/test -m ./model.h5
```

`-m` 参数用来指定持久化的自编码器网络参数。

## train

自编码器的训练可以使用 `./autoencoder.ipynb`。

它分别使用 `./dataset/train` 以及 `./dataset/test` 下的图片作为训练集和验证集。

默认迭代 2000 次，然后保存模型参数。

同时会绘制训练过程中的损失值，以及给出在验证集上的去噪表现图片。

当你准备好下一阶段（识别网络）的数据集后，可以使用 `./captcha.ipynb` 来训练识别网络。

它分别使用 `./dataset1/train` 以及 `./dataset1/test` 下的图片作为训练集和验证集。

接下来，你可以手动添加代码，来保存网络参数，或直接进行预测。
