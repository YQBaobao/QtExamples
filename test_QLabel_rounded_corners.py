#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtExamples
@ File        : test_QLabel_rounded_corners.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : QLabel 中显示圆角效果的图片
"""
from typing import Union

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath

from PyQt5.QtWidgets import QWidget


def create_rounded_pixmap(pixmap: QPixmap, radius: Union[int, float]) -> QPixmap:
    """带圆角的 QPixmap"""
    if pixmap.isNull():  # 不处理空数据或者错误数据
        return pixmap

    # 获取图片尺寸
    image_width = pixmap.width()
    image_height = pixmap.height()

    # 处理大尺寸的图片,保证图片显示区域完整
    new_pixmap = QPixmap(
        pixmap.scaled(image_width, image_width if image_height == 0 else image_height, Qt.IgnoreAspectRatio,
                      Qt.SmoothTransformation))
    dest_image = QPixmap(image_width, image_height)
    dest_image.fill(Qt.transparent)

    painter = QPainter(dest_image)
    painter.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
    painter.setRenderHint(QPainter.SmoothPixmapTransform)  # 平滑处理
    # 裁圆角
    path = QPainterPath()
    rect = QRectF(0, 0, image_width, image_height)
    path.addRoundedRect(rect, radius, radius)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, image_width, image_height, new_pixmap)

    return dest_image


class RoundedQLabel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel()
        label.setText("圆角 QPixmap")
        label.setScaledContents(True)  # 自适应大小

        pixmap = QPixmap(r'F:\Projects\QtMiHoYoLauncher\testting\image\30.png')  # 替换为你的图像路径
        rounded_pixmap = create_rounded_pixmap(pixmap, 45)

        # 正方形图片
        # pixmap = QPixmap(r'F:\Projects\QtMiHoYoLauncher\testting\image\29.png')  # 替换为你的图像路径
        # rounded_pixmap = create_rounded_pixmap(pixmap, pixmap.height() / 2)

        label.setPixmap(rounded_pixmap)
        label.setFixedSize(pixmap.width() // 2, pixmap.height() // 2)  # 示例固定大小

        # 将 QLabel 添加到布局中
        layout.addWidget(label)
        self.setLayout(layout)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout

    app = QApplication([])
    window = RoundedQLabel()
    window.show()
    app.exec_()
