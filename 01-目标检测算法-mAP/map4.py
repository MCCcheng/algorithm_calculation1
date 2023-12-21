# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: map4.py
@time: 2023/12/11 17:58
@desc: 
"""
import numpy as np


def calculate_ap(recall, precision):
    """计算 Average Precision"""
    # 在 recall 值为 0 和 1 的时候插入点，确保区间为 [0, 1]
    recall = np.concatenate(([0.], recall, [1.]))
    precision = np.concatenate(([0.], precision, [0.]))

    # 保证 precision 对于 recall 的函数是非递增的
    if precision[0] < precision[-1]:
        precision = precision[::-1]
        recall = recall[::-1]

        # 计算面积
    area = np.trapz(precision, recall)
    # 计算平均值
    mean_pre = np.mean(precision)
    # 计算 Average Precision
    ap = mean_pre * area / np.sum(recall)
    return ap


def calculate_map(pred_boxes, gt_boxes, iou_threshold=0.5):
    """计算 mAP"""
    # 统计预测框和真实框的数量
    pred_num = len(pred_boxes)
    gt_num = len(gt_boxes)

    # 初始化 recall 和 precision 的数组
    recall = np.zeros(pred_num)
    precision = np.zeros(pred_num)

    # 对于每个预测框，计算与真实框的 IoU，并按照从小到大的顺序排序
    iou = calculate_iou(pred_boxes, gt_boxes, iou_threshold)
    iou_idx = np.argsort(iou)

    # 对于每个预测框，按照 IoU 的大小设置 recall 和 precision 的值
    for i in range(pred_num):
        recall[i] = iou[iou_idx[i]] / 1.0
        precision[i] = recall[i] if i == 0 else precision[i - 1] + (iou[iou_idx[i]] - recall[i - 1]) / (
                    recall[i] - recall[i - 1]) * (precision[i - 1] - precision[i - 2])

        # 计算 Average Precision，并返回 mAP 的值
    map_value = np.mean(calculate_ap(recall, precision)) * 100.0
    return map_value