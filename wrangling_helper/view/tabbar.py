from gui_utils.Qt import QtWidgets, QtGui, QtCore


class CustomTabBar(QtWidgets.QTabBar):

    change_name = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(CustomTabBar, self).__init__(parent=parent)

        self.setMovable(True)

    def change_tab_name(self, tab_index, name=None):
        if not name:
            name, accepted = QtWidgets.QInputDialog.getText(self, "Tab name", "New Tab name")
            if accepted and name:
                self.setTabText(tab_index, name)

    def mouseDoubleClickEvent(self, event):
        tab = self.tabAt(event.pos())
        self.change_tab_name(tab)
        self.change_name.emit(tab)
        super(CustomTabBar, self).mouseDoubleClickEvent(event)