from PyQt5.QtCore import Qt, QSize, QPoint, QFile, QTextStream
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QMainWindow, qApp, QStyle, QDesktopWidget


from .MainWindow_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # Frameless window
        self.setWindowFlags(Qt.WindowStaysOnTopHint |
                            Qt.FramelessWindowHint |
                            Qt.X11BypassWindowManagerHint)

        geometry = QStyle.alignedRect(Qt.LeftToRight,
                                      Qt.AlignCenter,
                                      QSize(220, 32),
                                      qApp.desktop().availableGeometry())
        self.setGeometry(geometry)

        # Transparent Background for the Window
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Set Font
        fontDB = QFontDatabase()
        fontDB.addApplicationFont(':/fonts/Fontin-Regular.ttf')
        fontDB.addApplicationFont(':/fonts/Fontin-SmallCaps.ttf')
        fontDB.addApplicationFont(':/fonts/TitilliumWeb-Bold.ttf')

        # Set Styling
        style_file = QFile(':/style.qss')
        style_file.open(QFile.ReadOnly | QFile.Text)
        self.setStyleSheet(QTextStream(style_file).readAll())
        style_file.close()

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
