import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import cv2

def CSVplotter():

    dir = "/Users/user/python/PIV/text/160-260"
    File_num = sum(os.path.isfile(os.path.join(dir,name)) for name in os.listdir(dir))


    for i in range(1,File_num+1):
        number = str("%04.f"%i)

        filename = "/Users/user/python/PIV/text/160-260/COUPLE"+number+".txt"
        df = pd.read_table(
            filename,
            encoding="shift-jis",
            sep=",",
            skiprows=[0,1,2,3,4,5,6,7,8,9],
            names=["NoJ","NoI","startX","startY","endX","endY","velocity","degree","velocityX","velocityY","UZUDO","HASSANRYO"])

        df = df.iloc[:18104,2:]
        #df = df.iloc[25:30,]

        df = df.replace("     ---", "NaN")
        df = df.replace("      ---", "NaN")
        df = df.replace("       ---", "NaN")
        df = df.replace("        ---", "NaN")
        df = df.replace("         ---", "NaN")

        df = df.astype(float)
        print(df)


        df = df.dropna(axis=0)
        #print(df["velocityX"].unique())

        #print(df.describe())
        df["meanX"] = (df["endX"]+df["startX"])/2
        df["meanY"] = (df["endY"]+df["startY"])/2
        print(df)


        #df.plot.scatter(x="meanX", y="meanY")
        #img.show()
        #velocityX_fig = plt.scatter(df["meanX"], df["meanY"], s=5, c=df["velocityX"], cmap="magma")
        #plt.savefig("/Users/user/python/PIV/done/160-260/velocityX/COUPLE"+number+".png")
        #velocityY_fig = plt.scatter(df["meanX"], df["meanY"], s=5, c=df["velocityY"], cmap="magma")
        #plt.savefig("/Users/user/python/PIV/done/160-260/velocityY/COUPLE"+number+".png")
        #UZUDO_fig = plt.scatter(df["meanX"], df["meanY"], s=5, c=df["UZUDO"], cmap="magma")
        #plt.savefig("/Users/user/python/PIV/done/160-260/UZUDO/COUPLE"+number+".png")
        df.to_csv("/Users/user/python/PIV/done/160-260/CSV/COUPLE"+number+".csv")

        #cv2.imwrite("/Users/user/python/PIV/done/160-260/done/COUPLE"+number+".png", velocity_fig)

    return

CSVplotter()