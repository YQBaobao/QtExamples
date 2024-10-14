#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtExamples
@ File        : test_QFrame_Animation.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : QFrame 实现页面类抽屉式的进入与退出的动画
"""
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFrame, QGraphicsOpacityEffect
from PyQt5.QtCore import QRect, QPropertyAnimation


class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName("Window")
        Window.resize(800, 200)

        # 创建按钮触发进入动画
        self.start_button = QPushButton(Window)
        self.start_button.setText("进入")
        self.start_button.setGeometry(QRect(330, 10, 130, 23))

        # 创建按钮触发退出动画
        self.exit_button = QPushButton(Window)
        self.exit_button.setText("退出")
        self.exit_button.setGeometry(QRect(330, 40, 130, 23))

        # 创建QFrame当做背景，模拟页面底层
        self.frame_bg = QFrame(Window)
        self.frame_bg.setGeometry(0, 70, 800, 130)
        self.frame_bg.setStyleSheet("background-color: red;")  # 背景色

        # 创建QFrame，模拟抽屉层
        self.frame = QFrame(Window)
        self.frame.setStyleSheet("background-color: lightblue;")  # 背景色


class Window(QWidget, Ui_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 设置 QFrame 为透明,然后后续在动画边修改透明度，边移动
        self.opacity_effect = QGraphicsOpacityEffect()
        self.frame.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)  # 初始透明度为0（完全透明）

        self.start_button.clicked.connect(self.start_animation)
        self.exit_button.clicked.connect(self.exit_animation)

    def start_animation(self):
        # 设置QFrame的geometry属性
        self.move_animation = QPropertyAnimation(self.frame, b"geometry")
        self.move_animation.setDuration(200)  # 动画持续时间为200ms
        self.move_animation.setStartValue(QRect(50, 110, 700, 120))  # 动画开始时的位置
        self.move_animation.setEndValue(QRect(50, 70, 700, 120))  # 动画结束时的位置

        # 设置QFrame的透明度属性
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)  # 动画持续时间为200ms
        self.opacity_animation.setStartValue(0)  # 动画开始时的透明度（完全透明）
        self.opacity_animation.setEndValue(1)  # 动画结束时的透明度（完全不透明）

        # 启动动画
        self.move_animation.start()
        self.opacity_animation.start()

    def exit_animation(self):
        # 设置QFrame的geometry属性
        self.move_animation = QPropertyAnimation(self.frame, b"geometry")
        self.move_animation.setDuration(200)  # 动画持续时间为200ms
        self.move_animation.setStartValue(QRect(50, 70, 700, 120))  # 动画开始时的位置
        self.move_animation.setEndValue(QRect(50, 110, 700, 120))  # 动画结束时的位置

        # 设置QFrame的透明度属性
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(200)  # 动画持续时间为200ms
        self.opacity_animation.setStartValue(1)  # 动画开始时的透明度（完全不透明）
        self.opacity_animation.setEndValue(0)  # 动画结束时的透明度（完全透明）

        # 启动动画
        self.move_animation.start()
        self.opacity_animation.start()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
