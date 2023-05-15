import cv2
#import numpy as np
from IPython import display
import matplotlib.pyplot as plt
#from PIL import Image
import os

def imshow(img, format=".BMP", **kwargs):
    """ndarray 配列をインラインで Notebook 上に表示する。
    """
    img = cv2.imencode(format, img)[1]
    img = display.Image(img, **kwargs)
    display.display(img)

dir = r'C:\Users\i054fb\HSCVD\20221122'
File_num = sum(os.path.isfile(os.path.join(dir,name)) for name in os.listdir(dir))


for i in range(1,File_num+1):
    number = str("%04.f"%i)
   
    img = cv2.imread(r"C:\Users\i054fb\HSCVD\20221122\Nov22_"+number+".bmp")
    #img2 = cv2.imread(r"C:\python\c4\1109_"+number2+".bmp")

    start_time = 0 #初期時間[s]
    time_rate = 60 #時間間隔[s]
    time = start_time + time_rate*i


    cv2.putText(img,
            text="t="+str(time)+"s",
            org=(100, 300),
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=4.0,
            color=(0, 0, 0),
            thickness=10,
            lineType=cv2.LINE_4)


    start_temp = 100 #撮影開始温度[℃]
    max_temp = 1400 +273 #撮影修了温度[℃]
    heating_rate = 100 #昇温速度[℃/min]
    temp = heating_rate * (i-1) + start_temp + 273

    if temp >= max_temp :
                #temp = max_temp
        cv2.putText(img,
            text="T="+str(max_temp)+"K",
            org=(100, 150),
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=4.0,
            color=(0, 0, 0),
            thickness=10,
            lineType=cv2.LINE_4)

    else:
        cv2.putText(img,
            text="T="+str(temp)+"K",
            org=(100, 150),
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=4.0,
            color=(0, 0, 0),
            thickness=10,
            lineType=cv2.LINE_4)


    cv2.imwrite(r"C:\Users\i054fb\HSCVD\20221122\done2\Nov22_"+number+".bmp",img)
    #cv2.imwrite(r"C:\python\MC18Photoshop\res\RUN0001_"+number+".bmp", img2)
    plt.show