from copy import deepcopy

from gui_utils.Qt import QtWidgets, QtCore, QtGui

"""
Base class for column delegates of various types.
"""
class TagDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self):
        super(TagDelegate, self).__init__()

    @staticmethod
    def color_variant(hex_color, brightness_offset=1):
        """ takes a color like #87c95f and produces a lighter or darker variant """
        if len(hex_color) != 7:
            raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
        rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
        new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
        new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
        # hex() produces "0x88", we want just "88"
        return new_rgb_int

    @staticmethod
    def color_luminance(r, g, b):
        return (0.299*r + 0.587*g + 0.114*b)

    def paint(self, painter, option, index):
        if not index.isValid():
            return
        rect = deepcopy(option.rect)
        self._draw_background(painter, option, index)
        self._draw_text(painter, option, index)

    def _draw_background(self, painter, option, index):
        rect = deepcopy(option.rect)
        path = QtGui.QPainterPath()
        path.addRoundedRect(rect, 3, 3)
        if option.state & QtWidgets.QStyle.State_Selected:
            background_color = QtGui.QBrush(option.palette.color(QtGui.QPalette.Highlight))
        else:
            background_color = index.data(QtCore.Qt.BackgroundRole)
        
        r, g, b, a = background_color.color().getRgb()
        color_luminance = TagDelegate.color_luminance(r, g, b)
        brightness = 50
        if color_luminance > 150:
            brightness = -50
        pen = QtGui.QPen(QtGui.QColor(*TagDelegate.color_variant(background_color.color().name(), brightness)))
        painter.setPen(pen)
        painter.fillPath(path, background_color)
        painter.drawPath(path)

    def _draw_text(self, painter, option, index):
        rect = deepcopy(option.rect)
        name = index.data(QtCore.Qt.DisplayRole)
        # pen = QtGui.QPen(QtCore.Qt.black)
        # painter.setPen(pen)
        painter.drawText(rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, name)

    def sizeHint(self, option, index):
        name = index.data(QtCore.Qt.DisplayRole)
        return QtCore.QSize(option.fontMetrics.width(name) + 8, 21)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    listwidget = QtWidgets.QListWidget()
    listwidget.setFlow(QtWidgets.QListView.LeftToRight)
    listwidget.setSpacing(3)
    listwidget.setItemDelegate(TagDelegate())
    for x in xrange(5):
        item = QtWidgets.QListWidgetItem()
        item.setText("Item number {}".format(x))
        item.setData(QtCore.Qt.BackgroundRole, QtGui.QBrush(QtGui.QColor("#444444")))
        listwidget.addItem(item)
    listwidget.show()
    app.exec_()
        

