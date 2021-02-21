# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtCore
from pyqtgraph.opengl import GLScatterPlotItem
from mainwindow import Ui_MainWindow
#from pi3dp import Pi3DP
from jog import Jog
from settings import Settings

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        #self.pi3dp = Pi3DP(None)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.tabWidget.tabBar().hide()

        self.ui.toolButtonMenuMain.clicked.connect( lambda : self.ui.tabWidget.setCurrentIndex(0) )
        self.ui.toolButtonMenuJog.clicked.connect( lambda : self.ui.tabWidget.setCurrentIndex(1) )
        self.ui.toolButtonMenuSettings.clicked.connect( lambda : self.ui.tabWidget.setCurrentIndex(2) )

        self.ui.tabWidget.widget(2).load_json('settings.json')

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
