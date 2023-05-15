# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 13:09:07 2022

@author: i054fb
"""

import os
import glob

# １．フォルダパス設定
in_folder = "/Users/user/python/PIV/RUN0018/0-20Fig/"

# ２．処理するファイル一覧情報を取得
file_list = glob.glob(in_folder + "*")

# ３．連番付与するための変数を初期化
cnt = 0
hold_page = ""

for f in sorted(file_list):
    # ４．f_titleにファイル名（拡張子なし）、f_extに拡張子
    f_title, f_ext = os.path.splitext(os.path.basename(f))
    now_page = f_title[1:4]

    # ５．連番設定（キーブレイク）
    if hold_page != now_page:
        cnt = 0
        hold_page = now_page
    cnt += 1
    
    word = "RUN_"
    f_ext = ".bmp"
    # ６．リネーム処理
    os.rename(f, os.path.join(
        in_folder, word + '{0:04d}'.format(cnt) + f_ext))