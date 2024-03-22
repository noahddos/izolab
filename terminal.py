import sys  
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import QtGui
from port import serial_ports,speeds
import serial 
import threading
import os
import matplotlib.pyplot as plt 

port = serial_ports()[0]
speed = 9600
writing_data = False
mypath = os.path.abspath(os.path.dirname(__file__))
path = f"{mypath}\output.txt"
arduino = serial.Serial()

def graph():
    with open(path) as file:
        arr = [list(map(float,i.split())) for i in file]
    temperature = []
    pressure = []
    volume = []
    for i in arr:
        pressure.append(i[1])
        temperature.append(i[0])
        volume.append(i[2])

    plt.figure(figsize=(12, 6), dpi=100)

    # first graph 
    plt.subplot(221)
    plt.plot(volume,pressure)
    plt.title('first')
    plt.xlabel('volume')
    plt.ylabel('pressure')

    # second graph 
    plt.subplot(222)
    plt.plot(temperature,pressure)
    plt.title('second')
    plt.xlabel('temperature')
    plt.ylabel('pressure')
    plt.xlim(10,45)

    #third graph 
    plt.subplot(313)
    plt.plot(volume,temperature)
    plt.title('third')
    plt.xlabel('volume')
    plt.ylabel('temperature')
    plt.ylim(10,45)
    plt.show() 

def writing():
    global path, arduino
    with open(path ,'w') as file:
        pass
    f = open(path,'w')
    while True:
        event = e.wait()
        while writing_data:
            f = open(path,'a')
            temp = list(map(str,str(arduino.readline())[2:-5].split()))
            if len(temp) == 3:
                [f.write(i.translate({ord(i): None for i in 'x\\fd'})+' ') for i in temp] # crutch 
                f.write('\n')
            f.close()  
        e.clear()

thr1 =threading.Thread(target= writing,daemon=True).start()
e = threading.Event()

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global line
        self.setWindowTitle("izo")
        self.setFixedSize(QSize(200,350))
        layout = QVBoxLayout()
    
        Port = QComboBox()
        Port.addItems(serial_ports())
        Speed = QComboBox()
        Speed.addItems(speeds)

        Port.currentTextChanged.connect(self.setport)
        Speed.currentTextChanged.connect(self.setspeed)

        ConnectButton = QPushButton('connect')
        ConnectButton.setCheckable(True)
        ConnectButton.clicked.connect(self.connect)
        ConnectButton.setFixedHeight(30)

        button_graph = QPushButton('get Graphs')
        button_graph.setCheckable(True)
        button_graph.clicked.connect(self.get_graph)
        button_graph.setFixedHeight(30)

        button_start = QPushButton('start write')
        button_start.setCheckable(True)
        button_start.clicked.connect(self.start_write)
        button_end = QPushButton('end write')
        button_end.setCheckable(True)
        button_end.clicked.connect(self.end_write)
        button_start.setFixedHeight(30)
        button_end.setFixedHeight(30)

        DataLine = QTextEdit()
        DataLine.setReadOnly(True)
        DataLine.resize(200,100)
        DataLine.setFixedHeight(100)
        DataLine.setContentsMargins(10,-70,0,0)
        DataLine.setText('data\n'*20)
        
        layout.addWidget(Port)
        layout.addWidget(Speed)
        layout.addWidget(ConnectButton)
        layout.addWidget(button_graph)
        layout.addWidget(button_start)
        layout.addWidget(button_end)
        layout.addWidget(DataLine)
    
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def start_write(self):
        try:
            global writing_data
            writing_data = True
            e.set()
        except:
            err2 = error2()
            err2.exec()

    def end_write(self):
        global writing_data
        writing_data = False

    def connect(self):
        try:
            global arduino
            arduino = serial.Serial(port,speed)
            success= Successed_connect()
            success.exec()
        except:
            err0 = error0()
            err0.exec()

    def setspeed(Self, s):
        global speed
        speed = int(s)

    def setport(Self, s):
        global port
        port = s

    def get_graph(self):
        try:
            graph()
        except:
            err1 = error1()
            err1.exec()
            

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()