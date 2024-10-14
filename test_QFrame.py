#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtExamples
@ File        : test_QFrame.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : QFrame 绘制聊天（三角）气泡，并显示文字
"""
from PyQt5.QtWidgets import QFrame, QLabel, QWidget, QVBoxLayout, QApplication
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import QPoint, Qt


class QFrameBubble(QFrame):
    def __init__(self, text='', parent=None):
        super().__init__(parent)
        self.pen = "#000000"  # 画笔颜色
        self.brush = "#E0F7FA"  # 笔刷颜色
        self.triangle_position = 'left'  # 三角形位置
        # 创建 QLabel 显示文字
        self.label = QLabel(text, self)
        self.label.setStyleSheet("background: transparent;")  # 设置背景透明
        self.label.setWordWrap(True)  # 如果文字过长，自动换行

        # 设置布局，将 QLabel 添加到 QFrameBubble 中
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.setContentsMargins(20, 10, 20, 10)  # 设置气泡内部边距
        self.setLayout(layout)
        # 设置无边框，以便自定义绘制
        self.setFrameStyle(QFrame.NoFrame)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # 设置画笔和笔刷
        pen = QPen(QColor(self.pen))
        painter.setPen(pen)
        brush = QBrush(QColor(self.brush))
        painter.setBrush(brush)

        # 绘制气泡的矩形部分
        rect = self.rect()
        rect.adjust(10, 10, -10, -10)  # 调整矩形的大小
        painter.drawRoundedRect(rect, 10, 10)

        if self.triangle_position == 'left':
            # 绘制气泡的三角部分在左侧中央
            points = [
                QPoint(rect.left(), rect.center().y() + 10),
                QPoint(rect.left() - 10, rect.center().y()),
                QPoint(rect.left(), rect.center().y() - 10)
            ]
        else:
            # 绘制气泡的三角部分在右侧中央
            points = [
                QPoint(rect.right(), rect.center().y() - 10),
                QPoint(rect.right() + 10, rect.center().y()),
                QPoint(rect.right(), rect.center().y() + 10)
            ]
        painter.drawPolygon(*points)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 200)

        # 创建自定义气泡
        bubble1 = QFrameBubble("聊天气泡,三角形在左侧", parent=self)

        bubble2 = QFrameBubble(parent=self)
        bubble2.pen = "#E0F7FA"
        bubble2.brush = "#E0F7FA"
        bubble2.triangle_position = 'right'
        bubble2.label.setText('聊天气泡,三角形在右侧')
        bubble2.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(bubble1)
        layout.addWidget(bubble2)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    window = Example()
    window.show()
    app.exec_()
