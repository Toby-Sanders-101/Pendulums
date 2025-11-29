from typing import List
from vectors import *
from colour_cls import *
from object_cls import *
from camera import Camera
from field_cls import *

class System3:
    def __init__(self, objects: List[Mass], strings: List[InelasticLightString], springs: List[Spring], gravity: UniformGravitationalField,  dt, cam: Camera):
        self.dt = dt
        self.objects = objects
        self.strings = strings
        self.springs = springs
        self.cam = cam
        cam.masses = objects
        cam.strings = strings
        cam.springs = springs
        self.gravity = gravity
        
        max_data_lines = 10
        self.time = 0
        self.app = QApplication(sys.argv)
        self.data_window = DataWindow(max_data_lines)
        self.data_window.show()

    def interpolate(self, _string): # this is to smoothen the transition from an object falling to being on a taught string but I'm not sure it'll work in all systems so maybe remove it
        print("interpolate string")
        for i in range(20):
            for body in self.objects:
                self.gravity.act_on(body)
            for spring in self.springs:
                spring.pull(self.dt/20)
            for string in self.strings:
                string.pull(self.dt/20)
            for body in self.objects:
                body.accelerate(self.dt/20)
                body.move(self.dt/20)

    def move_all(self):
        for body in self.objects:
            self.gravity.act_on(body)
        for spring in self.springs:
            spring.pull(self.dt)
        for string in self.strings:
            if string.pull(self.dt):
                self.interpolate(string)
        for body in self.objects:
            body.accelerate(self.dt)
            body.move(self.dt)

    def update_all(self):
        self.move_all()
        self.cam.display()
        self.time += self.dt
        #self.data_window.update_plot_data(self.time, self.objects[0].ke, self.objects[0].pe, self.objects[0].energy,
        #                                  self.objects[1].ke, self.objects[1].pe, self.objects[1].energy, 
        #                                  self.objects[0].energy+self.objects[1].energy)
        self.data_window.update_plot_data(self.time, self.objects[0].ke, self.objects[0].pe, self.objects[0].energy)
                                          #self.springs[0].epe, self.springs[0].epe+self.objects[0].energy)
        #print(self.strings[0].length)

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore
import pyqtgraph as pg

class DataWindow(QMainWindow):
    def __init__(self, max_data_lines):
        super(DataWindow, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.time = [0 for _ in range(1500)]
        self.ys = [[0 for _ in range(1500)] for _ in range(max_data_lines)]

        self.graphWidget.setBackground('w')

        self.data_lines = []
        for i in range(max_data_lines):
            self.data_lines.append(self.graphWidget.plot(self.time, self.ys[i], pen=pg.mkPen(color=Colour().tuple)))
        
        self.i = 0

    def update_plot_data(self, time, *args):
        self.time[self.i] = time
        for i in range(len(args)):
            self.ys[i][self.i] = args[i]
            self.data_lines[i].setData(self.time, self.ys[i])
        
        self.graphWidget.setXRange(max(0, time - 17), max(time,17))
        
        self.i += 1
        self.i %= 1500
