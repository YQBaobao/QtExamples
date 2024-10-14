#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtExamples
@ File        : test_QLabel_whirling.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 图像 360 度旋转
"""
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QFrame, QProgressBar
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import QTimer, Qt, QMetaObject, QCoreApplication

from examples.test_QLabel_rounded_corners import create_rounded_pixmap


class Ui_Whirling(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(712, 76)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")

        # 创建一个 QFrame，用于放置其余组件
        self.frame = QFrame(Form)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")

        # 网格布局
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")

        # 创建一个 QLabel，其实这个没啥用
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        # 创建一个 QProgressBar，其实这个没啥用
        self.progressBar = QProgressBar(self.frame)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 1, 1, 1, 1)

        # 创建一个 QLabel，用于实现图片旋转
        self.label = QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 2, 1)

        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "图片 360° 旋转"))
        self.label_2.setText(_translate("Form", "<<--- 左侧图片 360° 旋转"))
        self.label.setText(_translate("Form", "图片"))


class GIFRotatingLabel(QWidget, Ui_Whirling):
    """GIF实现"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        movie = QMovie(r"image\34.gif")  # 替换为你的图像路径
        self.label.setMovie(movie)
        movie.start()


class RotatingLabel(QWidget, Ui_Whirling):
    """QTransform"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        pixmap = QPixmap(r'image\20.png')  # 替换为你的图像路径，且必须是正方形

        # 创建圆形图像
        self.rounded_pixmap = create_rounded_pixmap(pixmap, pixmap.height() / 2)
        self.label.setPixmap(self.rounded_pixmap)  # 设置图像

        self.label.setFixedSize(pixmap.width(), pixmap.height())  # 设置 QLabel 的固定大小
        self.label.setAlignment(Qt.AlignCenter)  # 中心对齐

        self.angle = 0  # 初始角度

        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_image)
        self.timer.start(10)  # 每10毫秒更新一次

    def rotate_image(self):
        self.angle = (self.angle + 1) % 360  # 每次增加1度
        # transform = QTransform().rotate(self.angle)
        # 始终保持几何中心旋转
        transform = QTransform().translate(self.rounded_pixmap.width() / 2, self.rounded_pixmap.height() / 2) \
            .rotate(self.angle) \
            .translate(-self.rounded_pixmap.width() / 2, -self.rounded_pixmap.height() / 2)
        rotated_pixmap = self.rounded_pixmap.transformed(transform, mode=1)  # 使用平滑缩放
        self.label.setPixmap(rotated_pixmap)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = RotatingLabel()
    # window = GIFRotatingLabel()
    window.show()
    sys.exit(app.exec_())

