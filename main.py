import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5 import uic


class ControlPanel(QWidget):
    def __init__(self):
        super(ControlPanel, self).__init__()
        uic.loadUi('ui/control_widget.ui', self)


class Light(QWidget):
    def __init__(self):
        super(Light, self).__init__()
        uic.loadUi('ui/light.ui', self)


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('ui/main.ui', self)
        self.control_panel = ControlPanel()
        self.setWindowTitle('Ситифермы')
        self.scrollArea.setWidget(self.control_panel)
        self.light_view = Light()
        self.control_panel.lightButton.clicked.connect(self.light)
        self.control_panel.tempButton.clicked.connect(self.temp)
        self.handler.addWidget(self.light_view)
        pass

    def light(self):
        pass

    def temp(self):
        pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
sys.excepthook = except_hook
m = Main()
m.show()
sys.exit(app.exec())