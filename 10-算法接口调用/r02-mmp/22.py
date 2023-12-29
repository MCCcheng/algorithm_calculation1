# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: 22.py
@time: 2023/12/26 18:23
@desc: 
"""
from multiprocessing import Pool, current_process
import time
import random



a = 5
def task(a):
    a += 1
    print(a)


if __name__ == "__main__":
    p = Pool(processes=3, maxtasksperchild=3)
    p.apply_async(func=task, args=(a,))  # 进程池接收任务
    time.sleep(1)
    a =a+10
    p.apply_async(func=task, args=(a,))  # 进程池接收任务
    p.close()  # 关闭进程池 ==》 不接受任务
    p.join()  # 等待子进程执行完毕，父进程再执行
    print("end.............")