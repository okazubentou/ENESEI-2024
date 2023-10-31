import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import cv2
from glob import glob

####返り値を名前にすると関数が使いやすくなった！【2023/6/7】####
####○○ = 関数#####

def Picture_processing(im, Length):

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

    #界面から任意の距離離れた点(Marangoni=0, Finger=200)
    Optional_height = Average_height - Length
    return Optional_height

def DataFramer(Files_name, txt_number):

        #テキストファイルの読み込み
    filename = ""+Files_name+"/COUPLE"+txt_number+".txt"
    #txtをDataFlameに変換
    df = pd.read_table(
        filename,
        encoding="shift-jis",
        sep=",",
        skiprows=[0,1,2,3,4,5,6,7,8,9],
        names=["NoJ","NoI","startX","startY","endX","endY","velocity","degree","velocityX","velocityY","UZUDO","HASSANRYO"])
        #names=["NoJ","NoI","startX","startY","endX","endY","velocity","degree","sample","sample","UZUDO","HASSANRYO","ranryuX","ranryuY","ranryuEnergy"])
    
    #print(df)
    #左端の番号の行を排除
    df = df.iloc[:45632,2:]
    
    #欠損値をNaNにreplace
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
    #TXTファイルはstrであるためfloatに変換する．
    df = df.astype(float)

    return df

def plotter(num,value,Figure,dir_name, Length, total_num):

    ####グラフ作成####
    fig = plt.figure()
    #111は行，列，何番目か
    ax = fig.add_subplot(111)
    ax.plot(num, Figure)
    #凡例追加
    ax.set_xlabel("t [s]")
    plt.xlim(0,total_num//3)
    if value == 6:
        ax.set_ylabel("velocityX [mm/s]")
        title = "velocityX"
        plt.ylim(0,0.2)
    elif value == 7:
        ax.set_ylabel("sample [mm/s]")
        title = "sample"
        plt.ylim(0,0.2)
    elif value == 8:
        ax.set_ylabel("vorticity [/s]")
        title = "vorticity"
        plt.ylim(0,4)
        
    #軸の最大最小値を指定
    #plt.xlim(0,20)
    ####変える######
    #plt.ylim(0, 10)
    if Length == 0:
        plt.savefig(""+dir_name+"/test/Marangoni-"+title+".png")
    else:
        plt.savefig(""+dir_name+"/test/Finger-"+title+".png")

def tocsv(num,Figure,dir_name, Length):
    df = pd.DataFrame(data = {
                        "t[s]" : num, 
                        "vorticity[/s]" : Figure
                        })
    if Length == 0:
        kind = "Marangoni"
    elif Length == 100:
        kind = "Finger"
    else :
        kind = "unknown"
    
    df.to_csv(r""+dir_name+"/"+kind+".csv")

def texter(dir_name,num,Figure):

    df = pd.DataFrame(data = {
                        "t[s]" : num, 
                        "vorticity[/s]" : Figure
                        })
    
    with open(r""+dir_name+"/test.txt","a")as f:#データごとに書き換え

        f.write(str(df))

        f.write(" \n")

        f.close()

def Interfacer(dir_name,dir_num,Length,value):

    #各種定数
    Figure = []
    num = []
    kesson = 0
    span_s = 0
    span_f = 1280
    index_s = 0
    index_f = 40
    sample = 0
    sample_num = 0

    for dir in range(1, dir_num+1):

        dir_200 = dir*200

        number1 = str("%04.f"%dir_200)

        Files_name= r""+dir_name+"/PIV_res/"+number1+""
        File_num = sum(os.path.isfile(os.path.join(Files_name,name)) for name in os.listdir(Files_name))

        for i in range(1, File_num-1,1):
            #iは4桁の数値
            txt_number = str("%04.f" %i)
            pics_number = str("%04.f" %(i+(dir-1)*200))

            print(pics_number)
            im = cv2.imread(r""+dir_name+"/Pics/RUN_"+pics_number+".bmp")

            Optional_height = Picture_processing(im,Length)

            df = DataFramer(Files_name,txt_number)

            points = 0
            vorticity = 0

            for span in range (span_s, span_f+1,5):

                for index in range(index_s, index_f+1, 5):
               
                    height = Optional_height + index


                    if  df[(df["startX"] == span) & (df["startY"] == height)].empty == True:
                        kesson += 1
                    
                    else :
                        df = df.astype("float")
                        VEL = df[(df["startX"] == span) & (df["startY"] == height)]
                        #x方向速度は6、y方向速度は7、渦度は８
                        vorticity += abs(VEL.iloc[0,value])
                        #print(vorticity)
                        points += 1

            sample += (vorticity/points)
            #print(vorticity)
            print(points)
            sample_num += 1

            if sample_num == 3:
                Figure.append(sample/3)
                #print(sample/3)
                sample = 0
                sample_num = 0
                i_current = (dir-1)*200+i
                print(i_current,"枚目の処理が終了")
                i_time = i_current / 3
                num.append(i_time)


    tocsv(num, Figure, dir_name, Length)
    #texter(dir_name,num,Figure)


#インターフェイサーを実行 #マランゴニ：Length=0、密度差対流：Length=100
Interfacer(dir_name="C:/python/RUN0032",dir_num=5,Length=100,value=8)
