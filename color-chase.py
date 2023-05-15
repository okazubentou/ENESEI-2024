import cv2
import numpy as np
from IPython import display
import matplotlib.pyplot as plt
#from PIL import Image
import os

def imshow(img, format=".BMP", **kwargs):
    """ndarray 配列をインラインで Notebook 上に表示する。"""
    img = cv2.imencode(format, img)[1]
    img = display.Image(img, **kwargs)
    display.display(img)

dir = "/Users/user/HSCVD/wp90/"
File_num = sum(os.path.isfile(os.path.join(dir,name)) for name in os.listdir(dir))

for i in range(1,File_num):
    number = str("%04.f"%i)
   
    img = cv2.imread("/Users/user/HSCVD/wp90/RUN_"+number+".bmp")

    #画像のサイズを小さくする（前処理）
    height = img.shape[0]
    width = img.shape[1]
    img = resized_img = cv2.resize(img,(round(width/4), round(height/4)))
    
    #黄色を抽出
    yellow_hsv_min = np.array([40,100,100])
    yellow_hsv_max = np.array([70,255,255])

    #画像の2値化
    yellow_maskHSV = cv2.inRange(img,yellow_hsv_min,yellow_hsv_max)
    #cv2.imwrite(r"C:\python\data\wp10\yellow\RUN_"+number+".bmp",yellow_maskHSV)
    result = cv2.bitwise_and(yellow_maskHSV, yellow_maskHSV, mask=img_mask) 

    #茶色を検出
    brown_hsv_min = np.array([20,50,50])
    brown_hsv_max = np.array([40,100,100])

    #画像の2値化
    brown_maskHSV = cv2.inRange(img,brown_hsv_min,brown_hsv_max)
    #cv2.imwrite(r"C:\python\data\wp10\brown\RUN_"+number+".bmp",brown_maskHSV)

    #黒色を検出
    black_hsv_min = np.array([0,0,0])
    black_hsv_max = np.array([20,50,50])

    #画像の2値化
    black_maskHSV = cv2.inRange(img,black_hsv_min,black_hsv_max)
    #cv2.imwrite(r"C:\python\data\wp10\black\RUN_"+number+"_2.bmp",black_maskHSV)

    yellow = 0
    brown = 0
    black = 0
    total_pixel = 612*512

    for x in range(0,612,1):
    #1280
    
        for y in range (0,512,1):
        #960

            yellow_pixelValue = yellow_maskHSV[y, x]
            brown_pixelvalue = brown_maskHSV[y, x]
            black_pixelvalue = black_maskHSV[y, x]
        
            #blue = img[y, x, 0]
            #green = img[y, x, 1]
            #red = img[y, x, 2]
        
            if  yellow_pixelValue > 0 :
                yellow += 1

            elif brown_pixelvalue > 0 :
                brown += 1

            elif black_pixelvalue > 0 :
                black += 1

    yellow_ratio = yellow/total_pixel * 100
    brown_ratio = brown/total_pixel *100
    black_ratio = black/total_pixel *100

    #print(pixelValue)        
    value = [yellow_ratio, brown_ratio, black_ratio]
    print(value)
#cv2.waitKey(0)
#cv2.destroyAllWindows()