# -*- coding:utf-8 -*-
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

from config import AIJE_ASR_API

model_type = "common_cn_16k"
dmid = "3be9b92408ac4d3ba954c8edd2d8d649"
url = AIJE_ASR_API["stage"]

my_log = logger_utils.TestingLogger(mode="w")


def print_datetime():
    from datetime import datetime
    # 获取当前时间
    now = datetime.now()
    # 格式化时间
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted_time)
    return formatted_time


def get_strftime(timestamp, start_timestamp=None):
    from datetime import datetime
    # 使用datetime.fromtimestamp()方法将时间戳转换为datetime对象
    dt = datetime.fromtimestamp(timestamp - ((start_timestamp - 57600) if start_timestamp else 0))
    # 使用strftime()方法将datetime对象格式化为字符串
    formatted_time = dt.strftime("%H:%M:%S")
    return formatted_time


def get_time():
    return time.time()


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
            # print(message)
            self.state = message['header']['name']
            if self.state == TaskStatus.SentenceBegin:
                print("on_sentence_begin")
            if self.state == TaskStatus.TranscriptionResultChanged:
                sentence = message['payload']['result']
                print("TranscriptionResultChanged {}".format(sentence))
            if self.state == TaskStatus.SentenceEnd:
                sentence = message['payload']['result']
                confidence = message['payload']['confidence']
                time1 = message['payload']['time']
                confidence = np.power(10, confidence)
                # if confidence > 0.5:
                print("SentenceEnd {} {} ,confidence:{:3.3f}".format(time1, sentence, confidence))
                # *********
                # my_log.info(sentence)
                # print(get_strftime(time.time(), self.st))
                print(f"当前语音在音频的时间：{time1 / 1000}")
                print(f"当前asr运行时间：{time.time() - self.st}")
                if ((time.time() - self.st) - time1 / 1000) > 10:
                    print(
                        f"分析超时，用时：{((time.time() - self.st) - time1 / 1000)}秒************************************")
                else:
                    print(f"分析用时：{((time.time() - self.st) - time1 / 1000)}秒")
                waste_time_list.append((time.time() - self.st) - time1 / 1000)
                print("#####################################################################################")
                # *********
                self.result.append([str(time), sentence])
                # self.result.append([str(time), sentence])
                self.final_result_buffer.append(sentence)

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
        start_signal["header"]["namespace"] = "SpeechTranscriber"
        start_signal["header"]["name"] = "StartTranscription"
        start_signal["header"]["task_id"] = self.task_id
        start_signal["header"]["dmid"] = dmid
        start_signal["payload"]["format"] = "pcm"
        start_signal["payload"]["model_type"] = self.model_type
        start_signal["payload"]["sample_rate"] = self.samplerate
        start_signal["payload"]["enable_intermediate_result"] = False
        start_signal["payload"]["enable_punctuation_prediction"] = False
        start_signal["payload"]["enable_inverse_text_normalization"] = False
        start_signal["payload"]["max_sentence_silence"] = 800
        body = json.dumps(start_signal)
        print(body)
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


def requestOnce(audio_path, model_type, time_interval=0.02):
    """
    time_interval=0.5
    """
    data, samplerate = sf.read(audio_path, dtype='int16')
    binary_data = data.tobytes()
    samplerate = 16000  # 采样率
    client = WebSocketClient(url, samplerate, model_type)
    client.send_start_signal(samplerate)
    client.send_audio(binary_data, samplerate, time_interval)
    client.send_stop_signal()
    client.wait()
    client.close()
    # print("requestOnce", threading.current_thread().ident, client.get_result())
    # return client.get_result()
    return "".join([x[1] for x in client.get_result()])  # 把所有句子合并成一段


if __name__ == '__main__':
    st = time.time()
    pur_dir = r"室外--东莞--20min"
    for f in os.listdir(pur_dir):
        waste_time_list = []
        audio_path = os.path.join(pur_dir, f)
        requestOnce(audio_path, model_type)
        my_log.info(f"文件{f}，耗时：{round(time.time() - st, 2)}秒")
        my_log.info(f"平均每句响应时间：{round(sum(waste_time_list) / len(waste_time_list), 4)}秒")
    print(f"耗时：{time.time() - st}s")
