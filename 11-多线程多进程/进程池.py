# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: demo2.py
@time: 2023/12/28 9:32
@desc: 
"""
from multiprocessing import Pool, current_process, Manager
import time


def produce_data(queue):
    for i in range(10):
        queue.put(i)


def consume_data(queue):
    while queue.qsize() > 0:
        data = queue.get()  # 注意：当get()拿不到数据时，会一直处于等待状态
        print(f"当前进程为：{current_process().name}, 队列获取数据为：{data},队列剩余数据为：{queue.qsize()}个！")
        time.sleep(0.01)


if __name__ == '__main__':
    print(f"主进程{current_process().name}开始执行！")
    queue = Manager().Queue(maxsize=20)  #  多进程队列，用于进程间的通信
    # 方法1 ：
    p = Pool(processes=6, maxtasksperchild=6)
    p.apply_async(produce_data, args=(queue,))
    time.sleep(1)
    for i in range(5):
        p.apply_async(consume_data, args=(queue,))

    p.close()  # 关闭进程池，防止将任何其他任务提交到池中。需要在join之前调用，否则会报ValueError: Pool is still running错误
    p.join()  # 等待进程池中的所有进程执行完毕
    print(f"主进程{current_process().name}结束！")

    # 方法2  ：
    with Pool(processes=6) as p:  # 创建进程池
        p.apply_async(produce_data, args=(queue,))
