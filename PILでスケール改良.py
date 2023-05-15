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
from PIL import Image, ImageDraw,ImageFont
import os

def overlay_text(img, text, font_path, font_size, font_color, stroke_color, stroke_width):
    font=ImageFont.truetype(font_path, font_size)
    draw=ImageDraw.Draw(img)

    font_w, font_h = font.getsize(text, stroke_width=stroke_width)
    img_w, img_h = img.size
    margin_height = 100
    margin_bottom = 100

    position = (margin_height, img_h - font_h - margin_bottom)

    draw.text(
        position, text,
        font=font
        #fill=stroke_color,
        #stroke_width=stroke_width * 2,
        #stroke_fill=font_color)
    )

    draw.text(
        position, text,
        font=font, 
        fill=font_color,
        stroke_width=stroke_width,
        stroke_fill=stroke_color)

    return img

def overlay_logo(img, path, scale):
    logo = Image.open(path)
    base_w, base_h  = img.size
    logo_w, logo_h  = logo.size

    logo_resized = logo.resize((int(logo_w * scale), int(logo_h * scale))) # リサイズ
    logo_resized_w, logo_resized_h  = logo_resized.size
    margin_bottom = 170
    img.paste(logo_resized, (1650, 1650), logo_resized)
    return img

#フォルダ内の画像の数を数える
dir = "/Users/user/HSCVD/wp90"
File_num = sum(os.path.isfile(os.path.join(dir,name)) for name in os.listdir(dir))

start_temp = 40 #撮影開始温度[℃]
max_temp = 300 +273 #撮影修了温度[℃]
heating_rate = 1 #昇温速度[℃/min]
logo_path = "/Users/user/HSCVD/Pics/300.png"
font_size = 400
font_path = '/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc'
font_color = (255,248,196) # 文字の色
stroke_color = (112, 96, 85) # 枠線の色
stroke_width = 10


#画像の数だけfor文で処理
for i in range(1,File_num, 100):
    number = str("%04.f"%i)

    img_path = "/Users/user/HSCVD/wp90/RUN_"+number+".bmp"
    out_path = "/Users/user/HSCVD/done/RUN_"+number+".bmp"

    temp = heating_rate * (i-1) + start_temp + 273

    #画像に温度記入
    if temp >= max_temp : 
        text=str(max_temp)+"K"
        img = overlay_logo(img_path, logo_path, 1.0)
        img = overlay_text(img, text, font_path, font_size, font_color, stroke_color, stroke_width)

    else:
        text=str(temp)+"K"
        img = overlay_logo(img_path, logo_path, 1.0)
        img = overlay_text(img, text, font_path, font_size, font_color, stroke_color, stroke_width)
        
    img.save(out_path)