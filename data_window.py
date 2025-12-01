from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore
import pyqtgraph as pg
import sys

class DataWindow(QMainWindow):
    def __init__(self, max_data_lines, dt):
        self.app = QApplication(sys.argv)
        super(DataWindow, self).__init__()

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.time = [0 for _ in range(4000)]
        self.ys = [[0 for _ in range(4000)] for _ in range(max_data_lines)]

        self.graphWidget.setBackground('w')

        self.dt = dt
        self.now = 0
        
        self.data_lines = []
        for i in range(max_data_lines):
            self.data_lines.append(self.graphWidget.plot(self.time, self.ys[i], pen=pg.mkPen(color=(120*i, 240-80*i, 0))))
        
        self.i = 0

    def update_plot_data(self, *args):
        self.now += self.dt
        self.time[self.i] = self.now
        for i in range(len(args)):
            self.ys[i][self.i] = args[i]
            self.data_lines[i].setData(self.time, self.ys[i])
        
        self.graphWidget.setXRange(max(0, self.now - 17), max(self.now, 17))
        
        self.i += 1
        self.i %= 4000
