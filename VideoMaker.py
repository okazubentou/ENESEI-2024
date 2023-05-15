import cv2

img_array = []

#読み込みたい画像ファイル
for i in range (1, 58+1):
    img = cv2.imread('/Users/user/python/PIV/RUN0018/0-20Fig/RUN_%04d.bmp' %i)
    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)

#動画のpathを指定
name = '/Users/user/python/PIV/RUN0018/RUN0018.mp4'
#VideoWriter(動画パス, 動画の拡張子, fps, 解像度)
out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'mp4v'), 10.0, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
