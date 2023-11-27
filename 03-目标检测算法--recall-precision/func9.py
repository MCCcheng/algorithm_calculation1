# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: func9.py
@time: 2023/10/18 16:53
@desc: 
"""
from sklearn.metrics import precision_recall_curve, roc_curve, auc
import matplotlib.pyplot as plt


def plt_pr(y_true, y_score):
    # 计算精确率、召回率和阈值
    precision, recall, thresholds = precision_recall_curve(y_true, y_score)

    # 绘制P-R曲线
    plt.plot(recall, precision)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.show()


def plt_roc(y_true, y_score):
    # 计算ROC曲线下的面积（AUC）
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)

    # 绘制ROC曲线
    plt.plot(fpr, tpr)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve (AUC = {:.2f})'.format(roc_auc))
    plt.show()


if __name__ == '__main__':
    y_true = [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0]  # 替换为真实标签列表
    y_scores = [0.3, 0.7, 0.3, 0.6, 0.8, 0.9, 0.56, 0.78, 0.65, 0.85, 0.59, 0.65]  # 替换为预测标签列表
    plt_pr(y_true, y_scores)
    plt_roc(y_true, y_scores)
