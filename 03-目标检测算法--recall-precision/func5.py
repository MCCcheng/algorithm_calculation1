# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: func5.py
@time: 2023/10/18 10:06
@desc: 
"""

from sklearn.metrics import precision_score, recall_score

# 假设你有以下真实标签和预测标签
y_true = [0, 1, 2, 0, 1, 2]  # 真实标签
y_pred = [0, 2, 1, 0, 0, 1]  # 预测标签

# 计算 micro 平均的精确率
precision_micro = precision_score(y_true, y_pred, average='micro')
print(f'Micro-average Precision: {precision_micro}')

# 计算 micro 平均的召回率
recall_micro = recall_score(y_true, y_pred, average='micro')
print(f'Micro-average Recall: {recall_micro}')

# 计算 macro 平均的精确率
precision_macro = precision_score(y_true, y_pred, average='macro')
print(f'Macro-average Precision: {precision_macro}')

# 计算 macro 平均的召回率
recall_macro = recall_score(y_true, y_pred, average='macro')
print(f'Macro-average Recall: {recall_macro}')