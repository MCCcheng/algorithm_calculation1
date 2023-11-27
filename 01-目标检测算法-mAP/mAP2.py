# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: 2.py
@time: 2023/8/31 17:18
@desc: 
"""

from sklearn.metrics import average_precision_score, precision_recall_curve
from sklearn.preprocessing import label_binarize
from sklearn.metrics import classification_report


def compute_map(y_true, y_pred, average="macro"):
    # 将标签二值化
    y_true = label_binarize(y_true, classes=[0, 1, 2, 3])
    y_pred = label_binarize(y_pred, classes=[0, 1, 2, 3])

    # 计算每个类别的AP
    aps = []
    for i in range(1, y_true.shape[1]):
        y_true_i = y_true[:, i]
        y_pred_i = y_pred[:, i]
        precision, recall, _ = precision_recall_curve(y_true_i, y_pred_i)
        ap = average_precision_score(y_true_i, y_pred_i)
        aps.append(ap)

        # 根据指定的平均方法计算mAP
    if average == "macro":
        return sum(aps) / len(aps)
    elif average == "micro":
        y_true = y_true.ravel()
        y_pred = y_pred.ravel()
        return average_precision_score(y_true, y_pred)
    else:
        raise ValueError("Invalid average option.")

    # 使用示例


y_true = [[0, 0, 1, 1], [0, 1, 1, 0], [0, 1, 1, 1]]
y_pred = [[0.1, 0.9, 0.05, 0.05], [0.1, 0.95, 0.05, 0.0], [0.1, 0.95, 0.05, 0.05]]
print(classification_report(y_true, y_pred))
print("mAP: {:.4f}".format(compute_map(y_true, y_pred)))