import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import uic


class ControlPanel(QWidget):
    def __init__(self):
        super(ControlPanel, self).__init__()
        uic.loadUi('ui/control_widget.ui', self)


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('ui/main.ui', self)
        # self.lightButton.setText('💡\nСвет')
        self.control_panel = ControlPanel()
        # self.lightButton.clicked.connect(self.light)
        self.scrollArea.setWidget(ControlPanel)


app = QApplication(sys.argv)
m = Main()
m.show()
sys.exit(app.exec())