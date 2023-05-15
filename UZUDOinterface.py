import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import cv2
from glob import glob


def Interfacer():

    dir_path = "/Users/user/python/PIV/RUN0018/"
    Files_name= ""+dir_path+"0-20sTEXT"
    File_num = sum(os.path.isfile(os.path.join(Files_name,name)) for name in os.listdir(Files_name))
    
    #x座標を指定)(320, 640, 960)
    POINT = 960

    velocityX_11 = []
    x = []
    num = []
    

    for i in range(1, File_num,1):
        #iは５桁の数値
        number = str("%04.f" %i)
        im = cv2.imread(""+dir_path+"0-20Fig/RUN_"+number+".bmp")

        #ガウシアンフィルタ
        gauss = cv2.GaussianBlur(im,(31, 31),0)
        #キャニー法
        minVal = 70
        maxVal = 70
        SobelSize = 10
        edges = cv2.Canny(gauss,minVal,maxVal,SobelSize)
        
        #白色部分の座標取得
        point = list(zip(*np.where(edges > 0)))
        point_change = sorted(point, key=lambda p:(p[1],p[0]))
        total_height = 0
        total_poiint = 0
        
        for x,y in point_change:
            total_height += x
            total_poiint += 1

        #画像の界面の平均値(左上を原点とする)
        Average_height = total_height / total_poiint
        correct = Average_height // 5
        Average_height = correct * 5

        #界面から任意の距離離れた点
        Optional_height = Average_height - 50

        #テキストファイルの読み込み
        filename = ""+Files_name+"/COUPLE"+number+".txt"
        #txtをDataFlameに変換
        df = pd.read_table(
            filename,
            encoding="shift-jis",
            sep=",",
            skiprows=[0,1,2,3,4,5,6,7,8,9],
            names=["NoJ","NoI","startX","startY","endX","endY","velocity","degree","velocityX","velocityY","UZUDO","HASSANRYO"])
            #names=["NoJ","NoI","startX","startY","endX","endY","velocity","degree","velocityX","velocityY","UZUDO","HASSANRYO","ranryuX","ranryuY","ranryuEnergy"])
        
        #print(df)
        #左端の番号の行を排除
        df = df.iloc[:45632,2:]

        df = df.replace(" ---", "NaN")
        df = df.replace("  ---", "NaN")
        df = df.replace("   ---", "NaN")
        df = df.replace("    ---", "NaN")
        df = df.replace("     ---", "NaN")
        df = df.replace("      ---", "NaN")
        df = df.replace("       ---", "NaN")
        df = df.replace("        ---", "NaN")
        df = df.replace("         ---", "NaN")
        df = df.replace("          ---", "NaN")
        df = df.replace("           ---", "NaN")
        df = df.replace("            ---", "NaN")
        df = df.replace("             ---", "NaN")

        #df = df.dropna(axis=0)
        #df = df.astype(float)

        #POINTの列番号を計算(ノート参照)
        Index_11 = int(((POINT/5)-3)+((Optional_height/5-4)*248)-1)
        
        #NaNでなければPOINTの要素を引っ張ってくる
        if df.iloc[Index_11,7] == "NaN":
            print("empty")
        
        else :
            df = df.astype(float) 
            POINT_11velocityX_11 = df[(df["startX"] == POINT) & (df["startY"] == Optional_height)]
            #POINT_11velocityX_11 = df[(df["startX"] == POINT_X2) & (df["startY"] == Optional_height)]
            #POINT_11 = df[(df["startX"] == POINT_X3) & (df["startY"] == Optional_height)]
            #print(POINT_11velocityX_11.iloc[0,6])
            
            velocityX_11.append(POINT_11velocityX_11.iloc[0,7])
            i = i / 2.9
            num.append(i)
    
    #print(velocityX_11)
    #print(num)
    velocityX = pd.DataFrame()
    velocityX["i"] = num
    velocityX["velocityX_11"] = velocityX_11
    #print(velocityX)
    velocityX.reset_index()

    ####グラフ作成####
    fig = plt.figure()
    #111は行，列，何番目か
    ax = fig.add_subplot(111)
    ax.plot(num, velocityX_11)
    #凡例追加
    ax.set_xlabel("t [s]")
    ax.set_ylabel("velocityY [mm/s]")
    #軸の最大最小値を指定
    plt.xlim(0,20)
    plt.ylim(-400, 400)
    plt.savefig(""+dir_path+"plt/velocityY13.png")

    #plt.show()



#インターフェイサーを実行
Interfacer()