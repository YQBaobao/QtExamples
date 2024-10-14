#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtExamples
@ File        : test_title_bar_dragging.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 
"""
import sys

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint


class FramelessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去掉窗口边框
        self.setGeometry(100, 100, 800, 600)

        # 创建一个 QFrame，用作拖动区域
        self.frame = QFrame(self)
        self.frame.setStyleSheet("background-color: lightgray;")
        self.frame.setGeometry(0, 0, 800, 50)  # 设置 QFrame 大小和位置

        # 用于记录鼠标拖动时的初始位置
        self.is_dragging = False
        self.drag_position = QPoint()

        # 为 QFrame 安装事件过滤器
        self.frame.installEventFilter(self)

    def eventFilter(self, source, event):
        # 处理 QFrame 上的鼠标事件
        if source == self.frame:
            if event.type() == event.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.is_dragging = True
                    self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                    event.accept()
                    return True

            elif event.type() == event.MouseMove:
                if self.is_dragging:
                    self.move(event.globalPos() - self.drag_position)
                    event.accept()
                    return True

            elif event.type() == event.MouseButtonRelease:
                self.is_dragging = False
                event.accept()
                return True

        return super().eventFilter(source, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FramelessWindow()
    window.show()
    sys.exit(app.exec_())
