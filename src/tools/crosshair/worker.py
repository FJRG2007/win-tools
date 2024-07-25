import os, sys, pystray, threading, win32api, win32con, win32gui
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from PIL import Image

class CrosshairWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.label = QLabel(self)
        self.image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Colors", "green.png")
        self.update_crosshair(self.image_path)
        self.show()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ensure_on_top_and_centered)
        self.timer.start(1000)

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        widget_geometry = self.geometry()
        self.move((screen_geometry.width() - widget_geometry.width()) // 2, (screen_geometry.height() - widget_geometry.height()) // 2)

    def update_crosshair(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull(): return print(f"Failed to load crosshair: {image_path}")
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.center()
    
    def ensure_on_top_and_centered(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.show()
        self.center()
        hwnd = int(self.winId())
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)


def quit_app(icon, item):
    icon.stop()
    QApplication.quit()

def change_crosshair(crosshair_widget, image_name):
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Colors", image_name)
    crosshair_widget.update_crosshair(image_path)

def create_system_tray_icon(crosshair_widget):
    colors_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Colors")
    alternative_crosshairs = ["green.png", "red.png", "blue.png", "pink.png", "black.png", "white.png"]

    menu_items = {}

    def create_menu_item(image_name):
        return pystray.MenuItem(image_name.capitalize().split('.')[0], lambda icon, item: change_crosshair(crosshair_widget, image_name),)

    for crosshair in alternative_crosshairs:
        menu_items[crosshair] = create_menu_item(crosshair)

    pystray.Icon("crosshair", Image.open(os.path.join(colors_path, "green.png")), "Lightweight Crosshair", menu=pystray.Menu(
        pystray.MenuItem("🎨 Colors", pystray.Menu(*menu_items.values())),
        pystray.MenuItem("✖️ Quit", quit_app)
    )).run()

def main():
    app = QApplication(sys.argv)
    crosshair_widget = CrosshairWidget()
    tray_thread = threading.Thread(target=create_system_tray_icon, args=(crosshair_widget,))
    tray_thread.daemon = True
    tray_thread.start()
    sys.exit(app.exec_())