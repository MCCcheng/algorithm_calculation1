# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: mAP.py
@time: 2023/8/29 17:47
@desc: 
"""
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve


def calculate_map(labels, predictions):
    """
    计算每个类别的AP，并返回mean AP。

    参数:
    labels: 二维数组，每行表示一个样本的真实标签。
    predictions: 二维数组，每行表示一个样本的预测标签。
    """
    # 计算每个类别的AP
    aps = []
    for i in range(labels.shape[1]):
        # 只考虑有真实标签的类别
        if np.sum(labels[:, i]) > 0:
            precision, recall, _ = precision_recall_curve(labels[:, i], predictions[:, i])
            ap = average_precision_score(labels[:, i], predictions[:, i])
            aps.append(ap)

            # 计算mean AP
    mAP = np.mean(aps)
    return mAP


if __name__ == '__main__':
    calculate_map(labels=[1,0,1,0,1,0,1,0],
                  predictions=[1,1,1,1,1,1,1,1])
    # calculate_map(labels=[],
    #               predictions=[1,1,1,1,1,1,1,1])