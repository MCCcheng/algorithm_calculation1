# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: func4.py
@time: 2023/8/17 15:13
@desc: 
"""
import re
import nltk
from my_utils import json_utils, file_utils


def calculate_cer(reference_chars, hypothesis_chars):
    """
    计算cer值
    """
    # 去除掉非中文字符
    reference_chars = remove_non_chinese_characters(reference_chars)  # 真实
    hypothesis_chars = remove_non_chinese_characters(hypothesis_chars)  # 预测
    # 使用nltk库计算编辑距离
    edit_distance = nltk.edit_distance(reference_chars, hypothesis_chars)
    # 计算CER
    cer = edit_distance / len(reference_chars) * 100
    return cer


def remove_non_chinese_characters(text):
    """
    去除掉非中文字符
    """
    pattern = r'[^\u4e00-\u9fff]'
    return re.sub(pattern, '', text)





if __name__ == '__main__':
    reference_chars = "你，好吗！我；们 ‘好"
    hypothesis_chars =  "你好吗我们好好"
    print(f"reference_chars:{len(reference_chars)}")
    print(f"hypothesis_chars:{len(hypothesis_chars)}")
    print(calculate_cer(reference_chars, hypothesis_chars))
