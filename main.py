# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtCore
from pyqtgraph.opengl import GLScatterPlotItem
import numpy as np
from gcode import Gcode
from mainwindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.graph.addItem(GLScatterPlotItem(pos=np.array([[0, 0, 0]]), size=0.1, color=(0.0, 1.0, 0.0, 0.5), pxMode=False))
        self.ui.graph.addItem(GLScatterPlotItem(pos=np.array([[0, 0, 0]]), size=1.0, color=(1.0, 0.0, 0.0, 1.0), pxMode=False))
        self.ui.graph.addItem(GLScatterPlotItem(pos=np.array([[0, 0, 0]]), size=2.0, color=(1.0, 1.0, 0.0, 1.0), pxMode=False))
        self.ui.graph.addItem(GLScatterPlotItem(pos=np.array([[0, 0, 0]]), size=2.0, color=(0.0, 1.0, 1.0, 1.0), pxMode=False))

        with open('test.gco', 'r') as f:
            self.gcode = Gcode( f.read() )

        self.ui.graph.items[0].pos = np.delete( self.gcode.print_lines[1], [3, 4, 5], 1 )
        self.ui.graph.items[1].pos = np.array( [self.gcode.print_lines[1][0][0:3]] )

        self.ui.horizontalSlider.setMaximum( len(self.gcode.print_lines[1]) - 1 )

        self.ui.toolButton.clicked.connect(self.start)
        self.ui.toolButton_2.clicked.connect(self.pause)

        self.ui.horizontalSlider.valueChanged.connect(self.slider_changed)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)

    def start(self):
        self.timer.start(1)

    def pause(self):
        self.timer.stop()

    def update(self):
        self.timer.stop()
        
        self.ui.horizontalSlider.setValue( self.ui.horizontalSlider.value() + 1 )
        self.slider_changed()

        self.timer.start(1)

    def slider_changed(self):
        value = self.ui.horizontalSlider.value()
        self.ui.horizontalSlider.setValue(value)
        self.ui.graph.items[1].pos = np.array( [self.gcode.print_lines[1][value][0:3]] )
        self.ui.graph.update()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()