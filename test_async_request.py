#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtExamples
@ File        : test_async_request.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 使用 aiohttp 发送异步请求
"""
import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QWidget
import aiohttp
from asyncqt import QEventLoop


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 80)
        self.setWindowTitle("PyQt5 使用 aiohttp")

        # 创建 QLabel QPushButton
        self.label = QLabel("按下按钮发出请求", self)
        self.button = QPushButton("发送 GET 请求", self)
        self.button.clicked.connect(self.handle_request)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def handle_request(self):
        # 在事件循环中运行异步函数
        asyncio.create_task(self.fetch_data())

    async def fetch_data(self):
        url = 'https://api.github.com/repos/YQBaobao/RollerCoaster/tags'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    tags = [tag['name'] for tag in data][:10]
                    # 更新标签
                    self.label.setText(f"Title: {tags}")
                else:
                    self.label.setText(f"请求失败: {response.status}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建 asyncio 事件循环
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()
    # sys.exit(app.exec_())
    # 在 asyncio 事件循环中运行应用程序
    with loop:
        loop.run_forever()
