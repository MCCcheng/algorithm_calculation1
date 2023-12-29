# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: demo2.py
@time: 2023/12/28 9:58
@desc: 
"""
"""
Process常用属性与方法：
 name:进程名
 pid：进程id
 run()，自定义子类时覆写
 start()，开启进程
 join(timeout=None)，阻塞进程
 terminate(),终止进程
 is_alive()，判断进程是否存活
线程锁---------------
lock = Lock()
lock.acquire()
lock.release()
"""
import time
import multiprocessing


def write_data(q):
    # 将列表元素写入到队列中
 for i in ['aa', 'bb', 'cc', 'dd']:
        print('开始写入值%s' % i)
        q.put(i)
        time.sleep(1)


def read_data(q):
    print("开始读取数据...")
    while True:
        if not q.empty():
            print("读取到数据：", q.get())
            time.sleep(1)
        else:
            break


if __name__ == '__main__':
    # 创建队列
    q = multiprocessing.Queue()
    # 创建进程
    qw = multiprocessing.Process(target=write_data, args=(q,))
    qr = multiprocessing.Process(target=read_data, args=(q,))
    # 启动进程
    qw.start()
    qr.start()
    qw.join()
    qr.join()