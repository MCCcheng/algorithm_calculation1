# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: recall-precision.py
@time: 2023/8/29 18:10
@desc: 
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve, roc_curve, auc


def main():
    # 随机生成真实标签和预测概率
    y_true = np.random.randint(0, 2, size=100)
    y_scores = np.random.rand(100)
    print(y_true)
    print(y_scores)

    # 计算准确率和召回率
    precision, recall, _ = precision_recall_curve(y_true, y_scores)
    ap = np.mean(precision[1:])  # 计算平均精确度
    recall_mean = np.mean(recall)  # 计算平均召回率

    # 计算PR曲线下的面积（AP）和ROC曲线下的面积（AUC）
    ap_score = auc(recall, precision)
    roc_auc = auc(y_scores, y_true)

    # 绘制PR曲线和ROC曲线
    plt.plot(recall, precision, marker='.', label='PR curve (AP={:.3f})'.format(ap_score))
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall curve')
    plt.legend()
    plt.show()

    plt.plot(y_scores, y_true, marker='.', label='ROC curve (AUC={:.3f})'.format(roc_auc))
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.xlabel('Score')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curve')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
