from matplotlib.animation import FuncAnimation
from port import serial_ports,speeds
import matplotlib.pyplot as plt 
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import QtGui
import threading
import serial
import time 
import sys
import os 

path = f"{os.path.abspath(os.path.dirname(__file__))}\output.txt"
arduino = serial.Serial()
writing_data = False
graph_update = False
port = serial_ports()
speed = speeds[0]

class error0(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("error")

        self.layout = QVBoxLayout()
        message = QLabel("ERROR[0] maybe you have already connected or connected incorrectly")
        self.layout.addWidget(message)
        self.setLayout(self.layout)

class error1(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("error")

        self.layout = QVBoxLayout()
        message = QLabel("ERROR[1] trable with graph.py. Check it out readme.txt to solve problem")
        self.layout.addWidget(message)
        self.setLayout(self.layout)

class error2(QDialog):
    def __init__(self,s):
        super().__init__()
        self.setWindowTitle("error")

        self.layout = QVBoxLayout()
        message = QLineEdit()
        message.setText(s)
        self.layout.addWidget(message)
        self.setLayout(self.layout)

class Successed_connect(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("success")

        self.layout = QVBoxLayout()
        message = QLabel(f"arduino is connected.\nwith {port}, {speed}")
        self.layout.addWidget(message)
        self.setLayout(self.layout)

class IZOLAB(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.setWindowTitle("IZOLAB")
        self.setFixedSize(QSize(200,200))
        self.layout = QVBoxLayout()

        self.Port = QComboBox()
        self.Speed = QComboBox()
        self.Port.setFixedHeight(40)
        self.Speed.setFixedHeight(40)

        self.ConnectButton = QPushButton()
        self.ConnectButton.setStyleSheet('QPushButton {background-color: #ffffff; color: black;}')
        self.ConnectButton.setText('not connected')
        self.ConnectButton.setCheckable(True)
        self.ConnectButton.setFixedHeight(40)

        self.buttonGraph = QPushButton('Graphs')
        self.buttonGraph.setStyleSheet('QPushButton {background-color: #ffffff; color: black;}')
        self.buttonGraph.setCheckable(True)
        self.buttonGraph.setFixedHeight(40)

        self.layout.addWidget(self.Port)
        self.layout.addWidget(self.Speed)
        self.layout.addWidget(self.ConnectButton)
        self.layout.addWidget(self.buttonGraph)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.Port.addItems(serial_ports())
        self.Speed.addItems(speeds)
        self.Port.currentTextChanged.connect(self.setPort)
        self.Speed.currentTextChanged.connect(self.setSpeed)
        self.ConnectButton.clicked.connect(self.connecting)
        self.buttonGraph.clicked.connect(self.getGraph)

    def connecting(self):
        try:
            global arduino
            arduino = serial.Serial(port,speed)
            self.ConnectButton.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
            self.ConnectButton.setText('connected')
        except:
            err0 = error0()
            err0.exec()
            
    def writeData(self):
        global writing_data
        if not(writing_data):
            self.buttonWriteData.setStyleSheet("background-color: red")
            writing_data = True
            self.thr.start()
        else:
            writing_data = False
            self.buttonWriteData.setStyleSheet("background-color: white")
            self.thr.terminate()
    
    def getGraph(self):
        global graph_update
        if not(graph_update):
            self.buttonGraph.setStyleSheet('QPushButton {background-color: #000000; color: white;}')
            graph_update = not(graph_update)
            graph()
        else:
            self.buttonGraph.setStyleSheet('QPushButton {background-color: #ffffff; color: black;}')
            graph_update = not(graph_update)

    def setPort(self,s):
        global port 
        port = s 
        print(port)

    def setSpeed(self,s):
        global speed
        speed = int(s)
        print(speed)
          
def main():
    app = QApplication(sys.argv)
    window = IZOLAB()
    window.show()
    app.exec()

def graph():
    global arduino, graph_update

    volume = []
    pressure = []
    temperature = []

    plt.ion()

    # first graph
    graph1 = plt.subplot(221)
    fst = graph1.plot(volume,pressure)
    plt.title('first')
    plt.xlabel('volume')
    plt.ylabel('pressure')

    # second graph
    graph2 = plt.subplot(222)
    snd = graph2.plot(temperature,pressure)
    plt.title('second')
    plt.xlabel('temperature')
    plt.ylabel('pressure')
    plt.xlim(10,45)

    graph3 = plt.subplot(313)
    trd = graph3.plot(volume,temperature)
    plt.title('third')
    plt.xlabel('volume')
    plt.ylabel('temperature')
    plt.ylim(10,45)

    plt.pause(3)
    line = list(map(float,arduino.readline().split()))
    volume.append(line[2])
    pressure.append(line[1])
    temperature.append(line[0])

    while(graph_update):
        line = list(map(float,arduino.readline().split()))
        if len(line) == 3 and (line[2] != volume[-1] or abs(line[1] - pressure[-1]) > 100 or abs(line[0] - temperature[-1]) > 0.1):
            print(line)
            volume.append(line[2])
            pressure.append(line[1])
            temperature.append(line[0])
            fst = graph1.plot(volume,pressure,color = 'r')[0]
            snd = graph2.plot(temperature,pressure,color = 'r')[0]
            trd = graph3.plot(volume,temperature,color = 'r')[0]
            plt.pause(0.2)
    plt.close()

if __name__ == '__main__':
    main()