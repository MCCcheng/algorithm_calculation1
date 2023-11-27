# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: class_.py
@time: 2023/9/13 15:15
@desc: 
"""
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score


class Target:
    """
    汇总了分类模型的测评指标
    """
    def __init__(self, y_true, y_pred):
        self.y_true = y_true
        self.y_pred = y_pred

    def accuracy_score(self):
        return accuracy_score(self.y_true, self.y_pred)

    def precision_score(self):
        return precision_score(self.y_true, self.y_pred)

    def recall_score(self):
        return recall_score(self.y_true, self.y_pred)

    def f1_score(self):
        return f1_score(self.y_true, self.y_pred)

    def confusion_matrix(self):
        return confusion_matrix(self.y_true, self.y_pred)

    def fnr(self):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return fn / (fn + tp)

    def fpr(self):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return fp / (fp + tn)

    def tnr(self):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return tn / (tn + fp)

    def tpr(self):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        return tp / (tp + fn)

    def new(self):
        from sklearn.metrics import precision_recall_curve
        precision, recall, thresholds = precision_recall_curve(y_true, y_score)


if __name__ == '__main__':
    y_true = [0, 1, 1, 0, 1]  # 实际标签
    y_pred = [0, 1, 1, 0, 1]  # 模型预测标签
    print(Target(y_true,y_pred).tpr())
