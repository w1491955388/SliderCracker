# -*- coding: utf-8 -*-
# @Time    : 2019/10/18 11:17
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : img_locate.py
# @Software: PyCharm

import os
import requests
from PIL import Image
import cv2
import numpy as np


def _pic_download(url, type):
    """
    图片下载
    :param url:
    :param type:
    :return:
    """
    img_path = os.path.abspath('...') + '\\' + '{}.jpg'.format(type)
    img_data = requests.get('https://verifycode.58.com' + url).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path


def get_distance(slider_url, captcha_url):
    """
    获取缺口距离
    :param slider_url:
    :param captcha_url:
    :return:
    """
    # 引用上面的图片下载
    slider_path = _pic_download(slider_url, 'slider')
    w, h = Image.open(slider_path).size

    # 图片还原
    captcha_path = _pic_download(captcha_url, 'captcha')

    # # 计算拼图还原距离
    target = cv2.imread(slider_path, 0)
    template = cv2.imread(captcha_path, 0)
    temp = 'temp.jpg'
    targ = 'targ.jpg'
    cv2.imwrite(targ, target)
    cv2.imwrite(temp, template)

    target = cv2.imread(targ)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    target = abs(255 - target)
    cv2.imwrite(targ, target)

    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)

    # 调用PIL Image 做测试
    image = Image.open(captcha_path)

    xy = (y, x, y + w, x + h)
    # 切割
    imagecrop = image.crop(xy)
    # 保存切割的缺口
    imagecrop.convert('RGB').save("new_image.jpg")
    imagecrop.show()
    return int(round(y))

