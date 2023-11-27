# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: func4.py
@time: 2023/10/18 9:54
@desc: 
"""
from sklearn.metrics import precision_score, recall_score, confusion_matrix

# 假设你有以下真实标签和预测标签
y_true = [0, 1, 1, 1, 0, 1]  # 真实标签
y_pred = [0, 1, 0, 1, 0, 1]  # 预测标签

# 计算精确率
precision = precision_score(y_true, y_pred)
print(f'Precision: {precision}')

# 计算召回率
recall = recall_score(y_true, y_pred)
print(f'Recall: {recall}')

# 计算混淆矩阵以可视化结果
cm = confusion_matrix(y_true, y_pred)
print('Confusion Matrix:')
print(cm)