# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: dsdsds.py
@time: 2023/10/17 10:41
@desc: 
"""

import cv2
import os


video_path = "path/to/video"
video = cv2.VideoCapture(video_path)

# 步骤5: 保存视频帧
frame_counter = 0
while True:
    ret, frame = video.read()  # 获取图片成功ret返回true，read()为迭代器，每次获取下一张图
    if not ret:
        break
    frame_path = f"frame_{frame_counter}.jpg"
    cv2.imwrite(frame_path, frame)
    frame_counter += 1

# 步骤6: 关闭视频文件
video.release()