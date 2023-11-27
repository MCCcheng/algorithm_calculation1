# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: func6.py
@time: 2023/10/18 10:24
@desc: 
"""

from sklearn.metrics import precision_score, recall_score

# # 假设你有以下真实标签和预测标签
# # y_true = [0, 1, 2, 0, 1, 2, 2]  # 真实标签
# # y_pred = [0, 2, 1, 0, 1, 2, 2]  # 预测标签
# y_true = [1, 2, 2, 1, 2, 0, 0]  # 真实标签
# y_pred = [1, 2, 2, 2, 1, 0, 0]  # 预测标签
#
# # 计算每个类别的精确率和召回率
# precision = precision_score(y_true, y_pred, average=None)
# recall = recall_score(y_true, y_pred, average=None)
#
# # 输出每个类别的精确率和召回率
# print('Precision: ', precision)
# print('Recall: ', recall)



y_true = ["好", "1", "1", "不好", "好", "不好", "好", "好", "好"]  # 真实标签
y_pred = ["好", "1", "1", "好", "不好", "不好", "好", "好", "好"]  # 预测标签

# 计算每个类别的精确率和召回率
precision = precision_score(y_true, y_pred, average=None)
recall = recall_score(y_true, y_pred, average=None)

# 输出每个类别的精确率和召回率
print('Precision: ', precision)
print('Recall: ', recall)