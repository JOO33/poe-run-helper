from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import QMainWindow, qApp, QStyle, QDesktopWidget

from .MainWindow_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.X11BypassWindowManagerHint
            )
        self.setGeometry(QStyle.alignedRect(
            Qt.LeftToRight, Qt.AlignCenter,
            QSize(220, 32),
            qApp.desktop().availableGeometry()))
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setupUi(self)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)

        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
