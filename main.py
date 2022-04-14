import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QButtonGroup
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPainter, QBrush, QColor
from PyQt5 import uic


class ControlPanel(QWidget):
    def __init__(self):
        super(ControlPanel, self).__init__()
        uic.loadUi('ui/control_widget.ui', self)


class Light(QWidget):
    def __init__(self, light):
        super(Light, self).__init__()
        uic.loadUi('ui/light.ui', self)
        self.light = light
        self.lineEdit.setText(f'{light} Лк')
        self.dial.setValue(int(light / 100))
        self.dial.valueChanged.connect(self.change)

    def change(self):
        self.light = self.dial.value() * 100
        self.lineEdit.setText(f'{self.light} Лк')

    def farm_change(self):
        self.dial.setValue(int(self.light / 100))
        self.lineEdit.setText(f'{self.light} Лк')


class Humidity(QWidget):
    def __init__(self):
        super(Humidity, self).__init__()
        uic.loadUi('ui/humidity.ui', self)
        self.humidity = None
        self.upButton_1.setIcon(QIcon('images/Arrow_Up.png'))
        self.upButton_2.setIcon(QIcon('images/Arrow_Up.png'))
        self.downButton_1.setIcon(QIcon('images/Arrow_Down.png'))
        self.downButton_2.setIcon(QIcon('images/Arrow_Down.png'))
        self.upButton_1.clicked.connect(self.air_up)
        self.upButton_2.clicked.connect(self.earth_up)
        self.downButton_1.clicked.connect(self.air_down)
        self.downButton_2.clicked.connect(self.earth_down)

    def air_up(self):
        if self.lcdNumber_1.value() != 100:
            self.lcdNumber_1.display(self.lcdNumber_1.value() + 5)
            self.humidity[0] += 5

    def air_down(self):
        if self.lcdNumber_1.value() != 0:
            self.lcdNumber_1.display(self.lcdNumber_1.value() - 5)
            self.humidity[0] -= 5

    def earth_up(self):
        if self.lcdNumber_2.value() != 100:
            self.lcdNumber_2.display(self.lcdNumber_2.value() + 5)
            self.humidity[1] += 5

    def earth_down(self):
        if self.lcdNumber_2.value() != 0:
            self.lcdNumber_2.display(self.lcdNumber_2.value() - 5)
            self.humidity[1] -= 5

    def farm_change(self):
        self.lcdNumber_1.display(self.humidity[0])
        self.lcdNumber_2.display(self.humidity[1])


class Temperature(QWidget):
    def __init__(self, temp):
        super(Temperature, self).__init__()
        uic.loadUi('ui/temperature.ui', self)
        self.temp = temp
        self.slider.setValue(int(temp / 30 * 100))
        self.slider.valueChanged.connect(self.put)
        self.label.setText(f'Текущая температура - {temp} °C')

    def put(self, change):
        self.temp = int(30 * self.slider.value() / 100)
        self.label.setText(f'Текущая температура - {self.temp} °C')
        self.repaint()

    def farm_change(self):
        self.slider.setValue(int(self.temp / 30 * 100))
        self.label.setText(f'Текущая температура - {self.temp} °C')

    def paintEvent(self, paint_event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(61, 74, 255)))
        size = self.size()
        h = int(self.temp / 30 * 350)
        painter.fillRect(size.width() // 2 - 30, size.height() // 2 - 175 + (350 - h), 60, h, QColor(61, 74, 255))
        self.slider.move(size.width() // 2 + 40, size.height() // 2 - 175)
        # painter.drawText(size.width() // 2 - 65, size.height() // 2 - 175, '30')
        n = 30
        for i in range(7):
            painter.drawText(size.width() // 2 - 65, size.height() // 2 - 175 + (350 // 6) * i, str(n))
            n -= 5


class Fans(QWidget):
    def __init__(self):
        super(Fans, self).__init__()
        uic.loadUi('ui/fan.ui', self)
        self.off = True
        self.onButton.clicked.connect(self.do_on)
        self.offButton.clicked.connect(self.do_off)

    def paintEvent(self, paint_event):
        if self.off:
            color = QColor('red')
        else:
            color = QColor('green')
        painter = QPainter(self)
        painter.setBrush(QBrush(color))
        w, h = self.size().width(), self.size().height()
        painter.drawEllipse(w // 2 - 100, h // 4 - 100, 200, 200)

    def do_on(self):
        self.off = False
        self.repaint()

    def do_off(self):
        self.off = True
        self.repaint()


class Adder(QWidget):
    def __init__(self):
        super(Adder, self).__init__()
        uic.loadUi('ui/adder.ui', self)
        self.farms_buttons = []
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.addButton)
        # self.groupBox.setLayout(self.horizontalLayout)
        self.current_farm = -1

    def add(self):
        button = QPushButton(f'Ферма {self.current_farm + 1}', parent=self)
        button.setFixedSize(93, 50)
        self.farms_buttons.append(button)
        self.horizontalLayout.addWidget(button)
        # self.groupBox.
        self.buttonGroup.addButton(self.farms_buttons[-1])

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('ui/main.ui', self)
        self.farms = []
        self.current_farm = 0
        self.control_panel = ControlPanel()
        self.setWindowTitle('Ситифермы')
        self.scrollArea.setWidget(self.control_panel)
        self.control_panel.lightButton.clicked.connect(self.light)
        self.control_panel.lightButton.setIcon(QIcon('images/bulb2.png'))
        self.control_panel.tempButton.setIcon(QIcon('images/temp2.png'))
        self.control_panel.humidButton.setIcon(QIcon('images/humidity.png'))
        self.control_panel.fanButton.setIcon(QIcon('images/fan.png'))
        self.deleteButton.setIcon(QIcon('images/thrash_bin.png'))
        self.control_panel.tempButton.clicked.connect(self.temp)
        self.control_panel.humidButton.clicked.connect(self.humid)
        self.control_panel.fanButton.clicked.connect(self.fan)
        self.adder = Adder()
        self.deleteButton.clicked.connect(self.delete)
        self.adder.addButton.clicked.connect(self.add)
        self.scrollArea_2.setWidget(self.adder)
        self.adder.buttonGroup.buttonClicked.connect(self.farm_change)

    def add(self):
        self.adder.current_farm += 1
        self.farms.append({
            'temp': 20,
            'light': 8000,
            'humidity': [75, 70],
            'fans': False
        })
        if len(self.farms) == 1:
            self.light_view = Light(self.farms[self.adder.current_farm]['light'])
            self.temp_view = Temperature(self.farms[self.adder.current_farm]['temp'])
            self.humid_view = Humidity()
            self.fans_view = Fans()
            self.humid_view.humidity = [75, 70]
            self.handler.addWidget(self.light_view)
            self.handler.addWidget(self.temp_view)
            self.handler.addWidget(self.humid_view)
            self.handler.addWidget(self.fans_view)
        else:
            self.light_view.light = self.farms[self.adder.current_farm]['light']
            self.temp_view.temp = self.farms[self.adder.current_farm]['temp']
            self.humid_view.humidity = self.farms[self.adder.current_farm]['humidity']
            self.fans_view.off = self.farms[self.adder.current_farm]['fans']
        self.adder.add()
        self.adder.buttonGroup.addButton(self.adder.farms_buttons[-1])

    def delete(self):
        self.adder.farms_buttons[self.current_farm].deleteLater()
        del self.adder.farms_buttons[self.current_farm]
        if not self.adder.farms_buttons:
            self.farms.clear()
            self.adder.current_farm = -1
            self.handler.removeWidget(self.light_view)
            self.handler.removeWidget(self.temp_view)
            self.handler.removeWidget(self.fans_view)
            self.handler.removeWidget(self.humid_view)

    def farm_change(self, button):
        if button.text() != '+':
            print(int(button.text().split()[-1]) - 1)
            data = self.farms[int(button.text().split()[-1]) - 1]
            self.farms[self.current_farm] = {
                'light': self.light_view.light,
                'temp': self.temp_view.temp,
                'humidity': self.humid_view.humidity,
                'fans': self.fans_view.off
            }
            self.light_view.light = data['light']
            self.temp_view.temp = data['temp']
            self.humid_view.humidity = data['humidity']
            # print(data['humidity'], self.humid_view.humidity)
            self.fans_view.off = data['fans']
            self.current_farm = int(button.text().split()[-1]) - 1
        self.light_view.farm_change()
        self.humid_view.farm_change()
        self.temp_view.farm_change()
        self.update()

    def light(self):
        self.handler.setCurrentIndex(0)

    def temp(self):
        self.handler.setCurrentIndex(1)

    def humid(self):
        self.handler.setCurrentIndex(2)

    def fan(self):
        self.handler.setCurrentIndex(3)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
sys.excepthook = except_hook
m = Main()
m.show()
sys.exit(app.exec())