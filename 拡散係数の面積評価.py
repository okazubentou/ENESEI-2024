# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 17:45:37 2021

@author: kandai419
"""


import cv2
#import numpy as np

for run in range (30,400,10):#データごとに書き換え
    number = str("%03.f"%run)
    
    
# readImage
    img = cv2.imread(r"C:\c4_res"+number+".bmp")
    #データごとに書き換え
    i = 0


    for x in range(0,612,1):
    #1280
    
        for y in range (0,512,1):
        #960

            pixelValue = img[y, x]
        
            blue = img[y, x, 0]
            green = img[y, x, 1]
            red = img[y, x, 2]
        
            if blue > 0 and green > 0 and red > 0:
           
                i = i + 1

    j = i / 1309560           

    print(j)
    
    with open("RUN0009.txt","a")as f:#データごとに書き換え
        
        f.write(str(j))
    
        f.write(" \n")

        f.close()
           
        
       