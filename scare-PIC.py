# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 13:21:57 2023

@author: ENESEI_MICROSCOPE
"""
#ライブラリをインポート
import cv2
#import numpy as np
from IPython import display
import matplotlib.pyplot as plt
from PIL import Image
import os

#フォルダ内の画像の数を数える
dir = "/Users/user/HSCVD/first"
File_num = sum(os.path.isfile(os.path.join(dir,name)) for name in os.listdir(dir))

#画像の数だけfor文で処理
for i in range(1,File_num):
    number = str("%04.f"%i)
   
    img = cv2.imread("/Users/user/HSCVD/first/RUN_"+number+".bmp")
  
    start_temp = 40 #撮影開始温度[℃]
    max_temp = 300 +273 #撮影修了温度[℃]
    heating_rate = 1 #昇温速度[℃/min]
    temp = heating_rate * (i-1) + start_temp + 273

    # OpenCV型 -> PIL型 ''
    new_image = img.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)

    img2 = Image.open("/Users/user/HSCVD/Pics/2mm.png")
    img2 = img2.resize((740,300))
    #imgにimg2を貼り付ける
    new_image.paste(img2, (800, 700), img2)

    new_image.save("/Users/user/HSCVD/first/done/RUN_"+number+".bmp")
