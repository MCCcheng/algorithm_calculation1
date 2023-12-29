# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: 11.py
@time: 2023/12/26 17:55
@desc: 
"""

from multiprocessing import Pool, current_process
import time
import random

lst = []


def task(i):
    print(current_process().name, i, 'start...')
    time.sleep(random.randint(1, 5))
    lst.append(i)
    print(lst)
    print(current_process().name, i, 'end.....')


if __name__ == "__main__":
    p = Pool(processes=3, maxtasksperchild=3)
    for i in range(10):
        p.apply_async(func=task, args=(i,))  # 进程池接收任务
    p.close()  # 关闭进程池 ==》 不接受任务
    print("dsdsddddddddddddddddddddddddd")
    p.apply_async(func=task, args=(777,))  # 进程池接收任务
    p.join()  # 等待子进程执行完毕，父进程再执行
    print("end.............")