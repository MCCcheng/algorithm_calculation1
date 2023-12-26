# -*- coding:utf-8 -*-
"""
@author: JunCheng
@file: demo2.py
@time: 2023/12/25 18:10
@desc: 
"""

import websocket


def on_message(ws, message):
    print("Received message:", message)


def on_error(ws, error):
    print("Error:", error)


def on_close(ws):
    print("Connection closed")


def on_open(ws):
    print("Connection opened")
    ws.send("Hello, server")


if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://example.com/ws",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()