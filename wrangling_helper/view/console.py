from gui_utils.Qt import QtWidgets, QtCore, QtGui, QtCompat
import os


_MAIN_UI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "ui", "console.ui")


class Console(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(Console, self).__init__(parent=parent)
        QtCompat.loadUi(_MAIN_UI, self)

    @property
    def console_widget(self):
        return self.loggerTE