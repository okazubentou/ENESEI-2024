import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerTuple

file = pd.read_table(
    "/Users/user/python/0912Tanoue.txt",
    comment="*",          # コメント開始の文字を1文字で指定
    encoding="shift-jis", # encoding は毎度明示的に指定したほうが良い
    sep="\s+",            # 空白区切りならこのように指定する
    header=None
)

xx = file.iloc[:,0]
file["Degree"]=xx
yy = file.iloc[:,1]
file["Height"]=yy

#データの変換，signal.argrelmax()関数がPandasのSeriesやDataFrameに対応していないため
x = np.array(xx)
y = np.array(yy)

x_max = max(xx)
y_max = max(yy)
y_min = min(yy)
x_min = min(xx)
plt.figure(figsize=(10,4))#図のアスペクト比を変更（横×縦）

#plt.bar(x,y, width=0.1)#棒グラフの図示　width=線の幅，デフォルトは0.8
plt.tick_params(labelsize = 9)#目盛りの数字の大きさを変更
plt.ylim(0, 120000)  # y 軸の範囲の設定,
plt.xlim(30,65) # x 軸の範囲の設定
        #plt.show()
plt.xlabel("2θ[°]" , fontsize = 10)
plt.ylabel("Intensity[cps]" , fontsize = 10)
   #plt.tight_layout()

#各変数
Threshold = 10000 #拾うymaxの最小値
Point_Height = 5000 #点の打つ高さ
Peak_order = 50 #極大値の感度

maxid = signal.argrelmax(y, order=50) #極大値 orderを変えることでピークの検出が変わる(ピーク検出の閾値)
#minid = signal.argrelmin(y, order=1) #極小値

dfx = pd.Series(x[maxid])
dfy = pd.Series(y[maxid])
df = pd.DataFrame([dfx, dfy])
df = df.T
df.columns = ['xmax', 'ymax']
print(df)

i=0
for i in range (0,len(df["xmax"])):
    if  36.00 <= df.iloc[i, 0] <= 37.00 or  39.00 <= df.iloc[i, 0] <= 41.00 or 42.00 <= df.iloc[i, 0] <= 43.00 or 50.00 <= df.iloc[i, 0] <= 51.00 or 54.50 <= df.iloc[i, 0] <= 56.00 or 59.00 <= df.iloc[i, 0] <= 61.00 or 64.00 <= df.iloc[i, 0] <= 65.00 or 45.00 <= df.iloc[i, 0] <= 46.00 and df.iloc[i,1]>=Threshold:
        dfx = df.iloc[i,0] #i行目のxmax
        dfy = df.iloc[i,1] #i行目のymax
        plt.plot(dfx,dfy+Point_Height,'o',label='SiO2',color='b')
        i = i+1

    elif 55.00 <= df.iloc[i, 0] <= 56.00 or 61.00 <= df.iloc[i, 0] <= 62.00 and df.iloc[i,1]>=Threshold:
        dfx = df.iloc[i,0] #i行目のxmax
        dfy = df.iloc[i,1] #i行目のymax
        plt.plot(dfx,dfy+Point_Height,'o',label='C',color='g')
        i = i+1

    elif df.iloc[i,1]>=Threshold :
        dfx = df.iloc[i,0]
        dfy = df.iloc[i,1]
        plt.plot(dfx,dfy+Point_Height,'o',label='another',color='r')
        i = i+1



handles, labels = plt.gca().get_legend_handles_labels()
labels = dict(zip(labels, handles))
plt.legend(labels.values(), labels.keys())

print(maxid)
plt.plot(x, y, linestyle='solid',color='r')   #x軸とy軸を指定
plt.savefig('/Users/user/python/0912Tanoue.png')    #保存
plt.close('all')