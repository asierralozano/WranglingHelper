from gui_utils.Qt import QtWidgets, QtCompat, QtCore, QtGui
import os
# from resources import resource


_MAIN_UI = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "ui", "create_tag.ui")


class CreateTagDialog(QtWidgets.QDialog):

    LABEL_COLOR_STYLESHEET = """
        border:1px solid lightgrey;
        background-color: {color}
    """

    def __init__(self, parent=None):
        super(CreateTagDialog, self).__init__(parent=parent)
        QtCompat.loadUi(_MAIN_UI, self)

        self._name = None
        self._color = None
        self.color_picker.clicked.connect(self._choose_color)
        self.tag_name_le.textChanged.connect(self._choose_name)

    def _choose_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color:
            self._color = color.name()
            stylesheet = CreateTagDialog.LABEL_COLOR_STYLESHEET.format(color=self._color)
            self.color_label.setStyleSheet(stylesheet)

    def _choose_name(self, text):
        self._name = text

    def showEvent(self, event):
        sG = QtWidgets.QApplication.desktop().screenGeometry()
        x = (sG.width()-self.width()) / 2
        y = (sG.height()-self.height()) / 2
        self.move(x,y)
        super(CreateTagDialog, self).showEvent(event)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wh = CreateTagDialog()
    # wh = BaseOption()
    # wh.start()
    wh.show()
    app.exec_()