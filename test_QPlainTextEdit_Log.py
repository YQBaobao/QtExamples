#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : Qt5Examples 
@ File        : test_QPlainTextEdit_Log.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : QPlainTextEdit 显示日志信息
"""

import sys
import logging
from typing import Callable

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser, QPlainTextEdit
from PyQt5.QtCore import pyqtSignal, QObject


class LogSignal(QObject):
    """日志信号"""
    log_signal = pyqtSignal(str)


class QtHandler(logging.Handler):
    """日志处理器"""

    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def emit(self, record):
        log_entry = self.format(record)
        self.signal.log_signal.emit(log_entry)


def init_log(update_log: Callable):
    """初始化日志系统"""
    log_signal = LogSignal()
    log_signal.log_signal.connect(update_log)  # 日志信号连接用于更新显示的槽函数

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 创建文件处理器，将日志写入文件
    file_handler = logging.FileHandler('application.log', encoding="utf-8")  # 文件处理器
    file_handler.setLevel(logging.DEBUG)  # 设置文件日志的级别
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    # 创建自定义处理器，就日志输出到 Qt 页面显示
    qt_handler = QtHandler(log_signal)  # 使用自定义的日志处理器
    qt_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(qt_handler)

    stream_handler = logging.StreamHandler()  # 输出到控制台
    stream_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s "))
    logger.addHandler(stream_handler)

    return logger


def fun_logging(logger):
    """使用举例：在方法中输出日志"""
    logger.info("这是一个方法中的 INFO 消息")
    logger.warning("这是一个方法中的 WARNING 消息")
    logger.error("这是一个方法中的 ERROR 消息")


class ClassLogging(object):
    """使用举例：在类中输出日志"""

    def __init__(self, logger):
        self.logger = logger

    def log_output(self):
        self.logger.info("这是一个类中的 INFO 消息")
        self.logger.warning("这是一个类中的 WARNING 消息")
        self.logger.error("这是一个类中的 ERROR 消息")


class LogWindow(QWidget):
    """显示日志的窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("日志输出")
        self.resize(600, 200)
        # self.log = QPlainTextEdit(self)
        self.log = QTextBrowser(self)
        self.log.setReadOnly(True)  # 设置为只读模式
        layout = QVBoxLayout()
        layout.addWidget(self.log)
        self.setLayout(layout)

        self.logger = init_log(self.update_log)  # 初始化日志
        # 举例
        self.logger.info("这是一个消息")
        #
        # 举例：在其他模块中输出日志
        fun_logging(self.logger)
        log_example = ClassLogging(self.logger)
        log_example.log_output()

    def update_log(self, log_text):
        # self.log.appendPlainText(log_text)  # 更新 QPlainTextEdit 内容
        self.log.append(log_text)  # 更新 QTextBrowser 内容

        # 将光标移动到文本的最后一行
        cursor = self.log.textCursor()
        cursor.movePosition(cursor.End)  # 移动光标到最后
        self.log.setTextCursor(cursor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogWindow()
    window.show()
    sys.exit(app.exec_())
