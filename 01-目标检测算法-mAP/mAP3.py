# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: mAP3.py
@time: 2023/10/31 17:54
@desc:


目标检测算法，怎么计算map值：

计算Mean Average Precision (mAP)是目标检测任务中常用的评估指标。mAP衡量的是在所有类别上的平均性能，并且对于每个类别的IoU阈值，都会计算一次AP，然后取平均值得到mAP。

以下是计算mAP的一般步骤：

计算每个类别的Precision-Recall曲线。首先，我们需要确定预测的边界框（bounding box）与真实的边界框（ground truth）的匹配程度。一般会使用IoU（Intersection over Union）来衡量，即预测框与真实框的交集面积与并集面积的比值。然后根据不同的IoU阈值，我们可以得到Precision-Recall曲线。
计算每个类别的AP。AP即Average Precision，是Precision-Recall曲线下的面积。具体来说，我们对Recall的值从0到1进行积分，得到AP。
计算mAP。最后，我们对所有类别的AP进行平均，得到mAP。
需要注意的是，在计算IoU时，我们通常只考虑预测框与真实框的中心点坐标和宽高的匹配程度，而不考虑偏移量。另外，在实际操作中，为了方便计算，我们通常会预设一个IoU的阈值列表，然后根据这个阈值列表来计算Precision-Recall曲线和AP。

以上步骤是标准的目标检测任务中计算mAP的方法。然而，不同的数据集可能有不同的计算方式，例如COCO数据集和Pascal VOC数据集就有所不同。因此，在实际操作中，需要参照所使用的数据集的具体规范来进行计算。
"""


