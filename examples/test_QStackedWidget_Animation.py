#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ Project     : QtExamples
@ File        : test_QStackedWidget_Animation.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description : 图片轮播动画
"""
from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect, QEvent, Qt, QTimer


class AnimatedStackedWidget(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.animation_duration = 500  # 动画持续时间（毫秒）
        self.current_animation = None  # 用于防止动画重叠

    def set_current_index_with_animation(self, index, direction='left'):
        current_index = self.currentIndex()

        if current_index == index or self.current_animation is not None:
            return

        # 获取当前页面和目标页面
        current_widget = self.currentWidget()
        next_widget = self.widget(index)

        # 确保目标页面的背景填充
        next_widget.setGeometry(self.rect())  # 使目标页面填充整个QStackedWidget
        next_widget.show()

        # 定义动画起始和结束位置
        width = self.width()
        if direction == 'left':
            current_end_pos = QRect(-width, 0, width, self.height())
            next_start_pos = QRect(width, 0, width, self.height())
        else:  # 'right'
            current_end_pos = QRect(width, 0, width, self.height())
            next_start_pos = QRect(-width, 0, width, self.height())

        # 当前页面淡出动画
        self.current_animation = QPropertyAnimation(current_widget, b"geometry")
        self.current_animation.setDuration(self.animation_duration)
        self.current_animation.setStartValue(current_widget.geometry())
        self.current_animation.setEndValue(current_end_pos)
        self.current_animation.setEasingCurve(QEasingCurve.OutCubic)

        # 下个页面淡入动画
        self.next_animation = QPropertyAnimation(next_widget, b"geometry")
        self.next_animation.setDuration(self.animation_duration)
        self.next_animation.setStartValue(next_start_pos)
        self.next_animation.setEndValue(self.rect())
        self.next_animation.setEasingCurve(QEasingCurve.OutCubic)

        # 动画结束时切换到目标页面
        def on_animation_finished():
            self.setCurrentIndex(index)
            current_widget.hide()
            self.current_animation = None  # 解除动画锁定

        # 连接动画结束信号到切换函数
        self.current_animation.finished.connect(on_animation_finished)

        # 启动动画
        self.current_animation.start()
        self.next_animation.start()


class Ui_DemoApp(object):
    def setupUi(self, DemoApp):
        DemoApp.setWindowTitle("轮播动画")
        DemoApp.resize(800, 200)
        self.stacked_widget = AnimatedStackedWidget(DemoApp)

        # 创建布局
        self.layout = QVBoxLayout(DemoApp)
        self.layout.addWidget(self.stacked_widget)

        # 添加页面
        page1 = QWidget()
        page1.setStyleSheet("background-color: #81bc88;")
        self.stacked_widget.addWidget(page1)
        page2 = QWidget()
        page2.setStyleSheet("background-color: #7a9dbc;")
        self.stacked_widget.addWidget(page2)
        page3 = QWidget()
        page3.setStyleSheet("background-color: #bc91a9;")
        self.stacked_widget.addWidget(page3)

        # 创建标签显示页码
        self.page_labels = [QLabel(f"{i + 1}", DemoApp) for i in range(self.stacked_widget.count())]
        for label in self.page_labels:
            label.setStyleSheet("color: gray;")  # 初始设置为暗淡的颜色
            label.setFixedSize(15, 15)
            label.setAlignment(Qt.AlignCenter)

        # 创建按钮
        self.button_next = QPushButton("下一页", DemoApp)
        self.button_prev = QPushButton("上一页", DemoApp)


class DemoApp(QWidget, Ui_DemoApp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 连接按钮事件
        self.button_next.clicked.connect(self.next_page)
        self.button_prev.clicked.connect(self.prev_page)

        # 隐藏按钮和标签初始状态
        self.button_next.hide()
        self.button_prev.hide()
        self.hide_current_page()

        # 高亮当前页码
        self.highlight_current_page()

        # 定时器设置
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_next_page)  # 自动轮播
        self.timer.start(3000)  # 每3秒切换一次

        # 安装事件过滤器到窗口
        self.installEventFilter(self)

    def auto_next_page(self):
        """自动切换到下一页"""
        self.next_page()

    def reset_timer(self):
        """重置定时器，以保持自动轮播"""
        self.timer.start(3000)

    def show_current_page(self):
        """显示标签页"""
        for label in self.page_labels:
            label.show()

    def hide_current_page(self):
        """隐藏标签页"""
        for label in self.page_labels:
            label.hide()

    def set_geometry_current_page(self):
        """设置标签页位置"""
        for i, label in enumerate(self.page_labels):
            label.setGeometry(self.width() // 2 + i * 15 - 30, self.height() - 45, 60, 30)

    def eventFilter(self, obj, event):
        """事件过滤，鼠标移入与移出"""
        if event.type() == QEvent.Enter and obj is self:
            # 鼠标进入时显示按钮
            self.button_next.show()
            self.button_prev.show()
            self.show_current_page()
        elif event.type() == QEvent.Leave and obj is self:
            # 鼠标离开时隐藏按钮
            self.button_next.hide()
            self.button_prev.hide()
            self.hide_current_page()
        return super().eventFilter(obj, event)

    def highlight_current_page(self, index=0):
        """更新标签样式"""
        for i, label in enumerate(self.page_labels):
            if i == index:
                label.setStyleSheet("color: black; font-weight: bold;")  # 高亮当前页码
            else:
                label.setStyleSheet("color: gray;")  # 暗淡其他页码

    def next_page(self):
        """下一页"""
        current_index = self.stacked_widget.currentIndex()
        next_index = (current_index + 1) % self.stacked_widget.count()
        self.stacked_widget.set_current_index_with_animation(next_index, direction='left')
        self.highlight_current_page(next_index)
        self.reset_timer()

    def prev_page(self):
        """上一页"""
        current_index = self.stacked_widget.currentIndex()
        prev_index = (current_index - 1) % self.stacked_widget.count()
        self.stacked_widget.set_current_index_with_animation(prev_index, direction='right')
        self.highlight_current_page(prev_index)
        self.reset_timer()

    def resizeEvent(self, event):
        """更新按钮位置"""
        super().resizeEvent(event)
        self.button_next.setGeometry(self.width() - 80, self.height() // 2 - 15, 60, 30)
        self.button_prev.setGeometry(20, self.height() // 2 - 15, 60, 30)
        self.set_geometry_current_page()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    demo = DemoApp()
    demo.show()
    sys.exit(app.exec_())
