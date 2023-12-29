# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: demo.py
@time: 2023/12/21 15:48
@desc: 
"""

import os.path
import time
import traceback
import websocket
import threading
import json
import soundfile as sf
import numpy as np
import uuid
from my_utils import file_utils, json_utils, logger_utils




class TaskStatus:
    SentenceBegin = 'SentenceBegin'
    SentenceEnd = 'SentenceEnd'
    TranscriptionResultChanged = 'TranscriptionResultChanged'
    TranscriptionCompleted = 'TranscriptionCompleted'
    Error = 'Error'
    Init = 'Init'
    Closed = 'Closed'
    Opened = 'Opened'


class WebSocketClient:
    def __init__(self, url):
        self.state = TaskStatus.Init
        self.init_ws(url)
        self.result = []
        self.st = time.time()

    def init_ws(self, url, ping_interval=500, ping_timeout=300):
        def on_message(ws, message):
            message = json.loads(message)
            print(message)

        def on_error(ws, error):
            print("######## on_error ############")
            self.state = TaskStatus.Error
            print(error)
            print(traceback.format_exc())
            self.ws.keep_running = False

        def on_close(ws, *args):
            print("######## on_close############")
            self.state = TaskStatus.Closed

        def on_open(ws):
            print("############# on_open #############")
            self.state = TaskStatus.Opened

        self.ws = websocket.WebSocketApp(
            url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )

        self.ws_thread = threading.Thread(target=self.ws.run_forever,
                                          args=(None, None, ping_interval, ping_timeout))

        self.ws_thread.daemon = True
        self.ws_thread.start()
        while (self.state == TaskStatus.Init):
            time.sleep(0.05)

    def send_start_signal(self):
        start_signal = {}
        start_signal["payload"]["max_sentence_silence"] = 800
        body = json.dumps(start_signal)
        self.ws.send(body)

    def send_stop_signal(self):
        stop_signal = {}
        stop_signal["header"] = {}
        body = json.dumps(stop_signal)
        self.ws.send(body)

    def send_audio(self):
        chunk_audio = ""
        self.ws.send(chunk_audio, opcode=websocket.ABNF.OPCODE_BINARY)

    def get_result(self):
        return self.result

    def wait(self, time_limit=-1):
        print("state", self.state)
        wait_time = 0
        while self.state != TaskStatus.TranscriptionCompleted and self.state != TaskStatus.Closed and self.state != TaskStatus.Error:
            time.sleep(0.1)
            wait_time += 0.1
            if wait_time >= time_limit != -1:
                print('wait time out')
                break

    def close(self):
        if self.ws_thread and self.ws_thread.is_alive():
            self.ws.keep_running = False
            self.ws_thread.join()
        self.ws.close()
        self.finish_time = time.time()


def main_task(audio_path):
    """
    time_interval=0.5
    """
    data, samplerate = sf.read(audio_path, dtype='int16')
    binary_data = data.tobytes()
    url = ""
    client = WebSocketClient(url)
    client.send_start_signal()
    client.send_audio()
    client.send_stop_signal()
    client.wait()
    client.close()
    return "".join([x[1] for x in client.get_result()])  # 把所有句子合并成一段


if __name__ == '__main__':
    audio_path = ""
    main_task(audio_path)

    # lock = Lock()
    # lock.acquire()
    # lock.release()