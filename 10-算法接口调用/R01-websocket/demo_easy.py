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
    def __init__(self, url, samplerate, model_type):
        self.task_id = uuid.uuid4().hex
        self.partial_result_buffer = []
        self.final_result_buffer = []
        self.result = []
        self.samplerate = samplerate
        self.model_type = model_type
        self.state = TaskStatus.Init
        self.init_ws(url)
        self.st = time.time()

    def init_ws(self, url, ping_interval=500, ping_timeout=300):
        def on_message(ws, message):
            message = json.loads(message)
            self.state = message['header']['name']
            if self.state == TaskStatus.SentenceEnd:
                sentence = message['payload']['result']
                confidence = message['payload']['confidence']
                time1 = message['payload']['time']
                confidence = np.power(10, confidence)

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

    def send_start_signal(self, samplerate):
        start_signal = {}
        start_signal["header"] = {}
        start_signal["payload"] = {}
        body = json.dumps(start_signal)
        self.ws.send(body)

    def send_stop_signal(self):
        stop_signal = {}
        stop_signal["header"] = {}
        stop_signal["header"]["namespace"] = "SpeechTranscriber"
        stop_signal["header"]["name"] = "StopTranscription"
        body = json.dumps(stop_signal)
        if self.state != TaskStatus.Closed and self.state != TaskStatus.Error:
            self.ws.send(body)

    def send_audio(self, audio_binary, samplerate, time_interval=0.02):
        # chunk_size = int(1280)
        chunk_size = int(samplerate * time_interval) * 2
        aduio_time = 0
        for i in range(0, len(audio_binary), chunk_size):
            aduio_time += time_interval
            send_time = time.time() - self.st
            time.sleep((aduio_time - send_time) if (aduio_time - send_time) > 0 else 0)  # 同步一下发送时间，跟视频时间一致；
            chunk_audio = audio_binary[i:i + chunk_size]
            if self.state != TaskStatus.Closed and self.state != TaskStatus.Error:
                self.ws.send(chunk_audio, opcode=websocket.ABNF.OPCODE_BINARY)
            # print(f"发送时间：{get_strftime(send_time)}")

    def get_result(self):
        return self.result

    def wait(self, time_limit=-1):
        print("state", self.state)
        wait_time = 0
        while :
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


def requestOnce(audio_path, model_type, time_interval=0.02):
    """
    time_interval=0.5
    """
    data, samplerate = sf.read(audio_path, dtype='int16')
    binary_data = data.tobytes()
    client = WebSocketClient(url, samplerate, model_type)
    client.send_start_signal(samplerate)
    client.send_audio(binary_data, samplerate, time_interval)
    client.send_stop_signal()
    client.wait()
    client.close()
    return "".join([x[1] for x in client.get_result()])  # 把所有句子合并成一段


if __name__ == '__main__':
    url = ""
    st = time.time()
    pur_dir = r"室外--东莞--20min"
    for f in os.listdir(pur_dir):
        waste_time_list = []
        audio_path = os.path.join(pur_dir, f)
        requestOnce(audio_path, model_type)
