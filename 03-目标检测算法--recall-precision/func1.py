# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: func1.py
@time: 2023/9/12 14:02
@desc: 
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.metrics import confusion_matrix

digits = datasets.load_digits()
X = digits.data
y = digits.target

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8)


from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)
log_reg.score(X_test, y_test)

y_predict = log_reg.predict(X_test)
cfm = confusion_matrix(y_test, y_predict)


# 矩阵变形处理：
    # 1)计算矩阵每一行的数据和；
row_sums = np.sum(cfm, axis=1)
    # 2）计算矩阵每一行的数据所站该行数据总和的比例；
err_matrix = cfm / row_sums
    # 3）让矩阵对角线的数据更改为0：因为对角线的数据全是模型预测正确的样本的数量，而分析混淆矩阵的主要目的是查看模型预测错误的地方；
        # np.fill_digonal(矩阵， m)：将矩阵对角线的数据全部改为 m；
np.fill_diagonal(err_matrix, 0)


plt.matshow(err_matrix, cmap=plt.cm.gray)
plt.show()