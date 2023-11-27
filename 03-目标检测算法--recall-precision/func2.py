# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: func2.py
@time: 2023/9/13 9:33
@desc: 
"""
import numpy as np
from my_utils.metrics.classification import plot_pr, plot_roc
from pybaseutils.metrics import class_report

true_labels = [0, 1, 2, 0, 1, 2, 2, 2, 1, 1, 1]  # 真实标签
pred_labels = [0, 2, 1, 0, 0, 1, 2, 2, 1, 1, 1]  # 预测标签
pred_scores = [0.8, 0.9, 0.7, 0.8, 0.8, 0.8,0.9,0.9,0.9,0.9,0.9]

# 计算混淆矩阵
conf_matrix = class_report.get_confusion_matrix(true_labels, pred_labels,
                                                filename="./confusion_matrix.cvs",
                                                normalization=False,
                                                plot=False,
                                                title="Confusion Matrix")

# 计算Accuracy、Precision、Recall、F1-Score
report = class_report.get_classification_report(true_labels, pred_labels,
                                                output_dict=False)
print(report)

plot_pr.plot_precision_recall_curve(true_labels, pred_scores)
plot_roc.plot_roc_curve(true_labels, pred_scores)
