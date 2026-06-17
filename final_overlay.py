import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QObject
from pynput import mouse


class SignalBridge(QObject):
    click_signal = pyqtSignal(int, int)
    clear_signal = pyqtSignal()


class FinalPoolOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.table_width = 224
        self.table_height = 432
        self.screen_width = QApplication.desktop().width()
        self.screen_height = QApplication.desktop().height()
        self.window_x = 100
        self.window_y = (self.screen_height - self.table_height) // 2
        self.clicked_point = None
        self.pockets = [
            (15, 15),
            (self.table_width - 15, 15),
            (15, self.table_height // 2),
            (self.table_width - 15, self.table_height // 2),
            (15, self.table_height - 15),
            (self.table_width - 15, self.table_height - 15)
        ]
        self.colors = [
            QColor(200, 200, 200, 100),
            QColor(200, 200, 200, 100),
            QColor(200, 200, 200, 100),
            QColor(200, 200, 200, 100),
            QColor(200, 200, 200, 100),
            QColor(200, 200, 200, 100)
        ]
        self.clear_timer = None
        self.bridge = SignalBridge()
        self.bridge.click_signal.connect(self.handle_click, Qt.QueuedConnection)
        self.bridge.clear_signal.connect(self.clear_lines, Qt.QueuedConnection)
        self.initUI()
        self.listener = mouse.Listener(on_click=self.on_global_click)
        self.listener.start()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(self.window_x, self.window_y, self.table_width, self.table_height)
        self.show()

    def clear_lines(self):
        self.clicked_point = None
        self.update()
        print("Lines cleared")

    def _timer_callback(self):
        self.bridge.clear_signal.emit()

    def on_global_click(self, x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            if self.window_x <= x <= self.window_x + self.table_width and \
               self.window_y <= y <= self.window_y + self.table_height:
                rel_x = x - self.window_x
                rel_y = y - self.window_y
                self.bridge.click_signal.emit(int(rel_x), int(rel_y))

    def handle_click(self, rel_x, rel_y):
        if self.clear_timer and self.clear_timer.is_alive():
            self.clear_timer.cancel()
        self.clicked_point = (rel_x, rel_y)
        print(f"Target: ({rel_x}, {rel_y})")
        self.clear_timer = threading.Timer(10.0, self._timer_callback)
        self.clear_timer.start()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(QColor(0, 150, 0, 60), 1)
        painter.setPen(pen)
        painter.drawRect(5, 5, self.table_width - 10, self.table_height - 10)
        if self.clicked_point:
            x, y = int(self.clicked_point[0]), int(self.clicked_point[1])
            for i, pocket in enumerate(self.pockets):
                pen = QPen(QColor(180, 180, 180, 60), 1)
                pen.setStyle(Qt.CustomDashLine)
                pen.setDashPattern([4, 8])
                painter.setPen(pen)
                painter.drawLine(x, y, pocket[0], pocket[1])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            if self.clear_timer and self.clear_timer.is_alive():
                self.clear_timer.cancel()
            self.listener.stop()
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = FinalPoolOverlay()
    print("Final Pool Overlay (224x432)")
    print("Click inside window area to draw lines")
    print("Lines auto-clear after 10 seconds")
    print("Press 'q' to quit")
    sys.exit(app.exec_())