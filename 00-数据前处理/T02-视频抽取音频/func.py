# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: 01-视频转音频.py
@time: 2023/8/18 14:35
@desc:
"""
import os
from pybaseutils.audio import audio_utils
from my_utils import file_utils


pur_dir = r"E:\岗评\test_data\原始视频"
save_dir = "my_audio_new2"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
for file_path in file_utils.get_file_path(pur_dir):
    file_name = file_utils.get_basename(file_path)
    save_name = file_utils.get_dirname(file_path).split("\\")[-1].replace("室内作业", "indoor")
    if "4号视角" in file_name:
        video_path = file_path
        audio_path = os.path.join(save_dir,f"{save_name}.wav")
        audio_utils.extract_video_audio(video_path, audio_path)
