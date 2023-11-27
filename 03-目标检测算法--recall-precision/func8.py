# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: func8.py
@time: 2023/10/18 14:48
@desc: 
"""

from sklearn.metrics import classification_report, confusion_matrix

# 假设真实标签为y_true，预测标签为y_pred
y_true = [0, 1, 2, 0, 1, 2]
y_pred = [0, 2, 1, 0, 1, 2]

# 计算混淆矩阵
cm = confusion_matrix(y_true, y_pred)
print("Confusion Matrix: ")
print(cm)

# 计算分类报告
report1 = classification_report(y_true, y_pred, output_dict=True)
report2 = classification_report(y_true, y_pred, output_dict=False)
print("Classification Report: ")
print(report2)
print(report1)