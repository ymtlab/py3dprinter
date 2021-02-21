# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtCore
from jog_widget import Ui_Form

class Jog(QtWidgets.QWidget):

    move_xyze       = QtCore.pyqtSignal(float, float, float, float)

    def __init__(self, parent=None):
        super(Jog, self).__init__(parent)
        
        self.mm_per_pulse_x = 0.0001
        self.mm_per_pulse_y = 0.0001
        self.mm_per_pulse_z = 0.0001
        self.mm_per_pulse_e = 0.0001

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.buttons = [
            self.ui.toolButtonXminus,
            self.ui.toolButtonXplus,
            self.ui.toolButtonYminus,
            self.ui.toolButtonYplus,
            self.ui.toolButtonXminusYminus,
            self.ui.toolButtonXminusYplus,
            self.ui.toolButtonXplusYminus,
            self.ui.toolButtonXplusYplus,
            self.ui.toolButtonZminus,
            self.ui.toolButtonZplus,
            self.ui.toolButtonEminus,
            self.ui.toolButtonEplus
        ]

        for func, button in [
            [lambda : self._move_xyze(-1,  0,  0,  0), self.ui.toolButtonXminus],
            [lambda : self._move_xyze( 1,  0,  0,  0), self.ui.toolButtonXplus],
            [lambda : self._move_xyze( 0, -1,  0,  0), self.ui.toolButtonYminus],
            [lambda : self._move_xyze( 0,  1,  0,  0), self.ui.toolButtonYplus],
            [lambda : self._move_xyze(-1, -1,  0,  0), self.ui.toolButtonXminusYminus],
            [lambda : self._move_xyze(-1,  1,  0,  0), self.ui.toolButtonXminusYplus],
            [lambda : self._move_xyze( 1, -1,  0,  0), self.ui.toolButtonXplusYminus],
            [lambda : self._move_xyze( 1,  1,  0,  0), self.ui.toolButtonXplusYplus],
            [lambda : self._move_xyze( 0,  0, -1,  0), self.ui.toolButtonZminus],
            [lambda : self._move_xyze( 0,  0,  1,  0), self.ui.toolButtonZplus],
            [lambda : self._move_xyze( 0,  0,  0, -1), self.ui.toolButtonEminus],
            [lambda : self._move_xyze( 0,  0,  0,  1), self.ui.toolButtonEplus]
        ]:
            button.clicked.connect(func)
            button.setAutoRepeat(True)
            button.setAutoRepeatDelay(1)
            button.setAutoRepeatInterval(1)

        self.ui.comboBoxSpeed.currentTextChanged.connect(self.speed_changed)
        self.ui.comboBoxType.currentTextChanged.connect(self.type_changed)

    def type_changed(self, text):
        if text == 'JOG':
            for button in self.buttons:
                button.setAutoRepeat(True)
        elif text == '1mm':
            for button in self.buttons:
                button.setAutoRepeat(False)
        elif text == '5mm':
            for button in self.buttons:
                button.setAutoRepeat(False)
        elif text == '10mm':
            for button in self.buttons:
                button.setAutoRepeat(False)

    def speed_changed(self, text):
        if text == 'Slow':
            self.mm_per_pulse_x = 0.0001
            self.mm_per_pulse_y = 0.0001
            self.mm_per_pulse_z = 0.0001
            self.mm_per_pulse_e = 0.0001
        elif text == 'Middle':
            self.mm_per_pulse_x = 0.001
            self.mm_per_pulse_y = 0.001
            self.mm_per_pulse_z = 0.001
            self.mm_per_pulse_e = 0.001
        elif text == 'Fast':
            self.mm_per_pulse_x = 0.01
            self.mm_per_pulse_y = 0.01
            self.mm_per_pulse_z = 0.01
            self.mm_per_pulse_e = 0.01

    def _move_xyze(self, x, y, z, e):
        dx, dy, dz, de = x * self.mm_per_pulse_x, y * self.mm_per_pulse_y, z * self.mm_per_pulse_z, e * self.mm_per_pulse_e
        self.ui.doubleSpinBoxX.setValue( self.ui.doubleSpinBoxX.value() + dx )
        self.ui.doubleSpinBoxY.setValue( self.ui.doubleSpinBoxY.value() + dy )
        self.ui.doubleSpinBoxZ.setValue( self.ui.doubleSpinBoxZ.value() + dz )
        self.ui.doubleSpinBoxE.setValue( self.ui.doubleSpinBoxE.value() + de )
        self.move_xyze.emit(dx, dy, dz, de)

def main():
    app = QtWidgets.QApplication(sys.argv)
    jog = Jog()
    jog.show()
    app.exec()

if __name__ == '__main__':
    main()
