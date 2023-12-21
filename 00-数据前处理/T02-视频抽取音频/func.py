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


pur_dir = r"test_source"
save_dir = "my_audio_new"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
for file_path in file_utils.get_file_path(pur_dir):
    save_name = file_utils.get_basename(file_path).replace("mp4", "wav")
    # save_name = file_utils.get_dirname(file_path).split("\\")[-1].replace("室内作业", "indoor")

    video_path = file_path
    audio_path = os.path.join(save_dir,f"{save_name}")
    audio_utils.extract_video_audio(video_path, audio_path)
