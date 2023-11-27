# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: func4.py
@time: 2023/8/17 15:13
@desc: 
"""
import os
from statistics import mean

import nltk

from my_utils import file_utils, json_utils


def calculate_cer(reference_chars, hypothesis_chars):
    # 将参考文本和识别结果转为字符列表
    reference_chars = reference.lower()
    hypothesis_chars = hypothesis.lower()

    # 使用nltk库计算编辑距离
    edit_distance = nltk.edit_distance(reference_chars, hypothesis_chars)

    # 计算CER
    cer = edit_distance / len(reference_chars) * 100
    return cer


def get_pd(p):
    with open(p, mode="r", encoding="utf-8") as f:
        data = f.read()
    content = [x.split(" ")[-1] for x in data.split("。")]
    content = "".join(content).replace("\n", "").replace("，", "").replace("。", "")
    return content


def get_gt(p):
    data = json_utils.load(p)
    content = ""
    for c in data:
        content += c["text"].replace("，", "").replace("。", "")
    return content


def show_compare(gt, pd):
    data = json_utils.load(gt)
    with open(pd, mode="r", encoding="utf-8") as f1:
        data1 = f1.readlines()
    for c1, c2 in zip(data, data1):
        print(c1["text"].replace("，", "").replace("。", ""))
        print(c2.replace("\n", "").replace("，", "").replace("。", ""))


if __name__ == '__main__':
    # 完整的
    gt_dir = r"E:\岗评\asr测试集\阿里\视频-aiasr\20220630indoor06.json"
    pd_path = r"E:\岗评\asr测试集\阿里\视频-aiasr\20220628indoor03_aiasr.txt"

    hypothesis = get_pd(pd_path)
    reference = get_gt(gt_dir)
    cer = calculate_cer(reference, hypothesis)

    print("reference：", reference)
    print("hypothesis：", hypothesis)
    print("reference字数：", len(reference))
    print("hypothesis字数：", len(hypothesis))
    print("cer:", cer)
