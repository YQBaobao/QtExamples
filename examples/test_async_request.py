#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtExamples
@ File        : test_async_request.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import aiohttp
from asyncqt import QEventLoop


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 with aiohttp Example")

        # Create UI elements
        self.label = QLabel("Press the button to make a request", self)
        self.button = QPushButton("Send GET Request", self)
        self.button.clicked.connect(self.handle_request)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def handle_request(self):
        # Run the asynchronous function in the event loop
        asyncio.create_task(self.fetch_data())

    async def fetch_data(self):
        url = 'https://gitee.com/api/v5/repos/yqbao/roller-coaster/tags?sort=name&direction=desc&page=1&per_page=5'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    # Update the label with the received data
                    tags = [tag['name'] for tag in data]
                    self.label.setText(f"Title: {tags}")
                else:
                    self.label.setText(f"Request failed with status: {response.status}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an asyncio event loop for PyQt5
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    # Run the application within the asyncio event loop
    with loop:
        loop.run_forever()
