from gui_utils.Qt import QtWidgets, QtCore, QtGui
from ..resources import resource
from ..resources.stylesheet.check_toolbutton import CHECK_TOOLBUTTON_STYLESHEET

class BaseOption(QtWidgets.QWidget):

    NAME = None
    DESCRIPTION = None
    RELATIVE = True
    DEPENDANT = None

    def __init__(self, parent=None):
        super(BaseOption, self).__init__(parent=parent)

        self._relative = False
        self._enabled = False
        self._option_widget = self.setup_option_widget()
        self._setup_ui()

    @property
    def relative(self):
        return self._relative

    @property
    def enabled(self):
        return self._enabled

    @property
    def option_widget(self):
        return self._option_widget

    def setup_option_widget(self):
        return QtWidgets.QLineEdit()

    def option_value(self):
        """Method that returns the Value of the option_widget
        
        Returns:
            Any: Depends of the widget
        """
        return None

    def set_option_value(self, value):
        pass

    def option_info(self, job=None):
        return None

    def export_info(self):
        export_info = dict()
        export_info.setdefault("enabled", self.enabled)
        export_info.setdefault("relative", self.relative)
        export_info.setdefault("value", self.option_value())
        return export_info        

    def _setup_ui(self):
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0,0,0,0)

        self.main_layout.addWidget(self.option_widget)

        relative_widget = self._setup_relative_button()
        self.main_layout.addWidget(relative_widget)

        enabled_widget = self._setup_enable_button()
        self.main_layout.addWidget(enabled_widget)

        info_widget = self._setup_info_button()
        self.main_layout.addWidget(info_widget)

        self.option_widget.setDisabled(True)
        relative_widget.setDisabled(True)

        if self.RELATIVE:
            enabled_widget.toggled.connect(relative_widget.setEnabled)
        
        enabled_widget.toggled.connect(self.option_widget.setEnabled)

    def _setup_relative_button(self):
        self._relative_button = QtWidgets.QPushButton()
        self._relative_button.setMinimumSize(QtCore.QSize(20, 20))
        self._relative_button.setMaximumSize(QtCore.QSize(20, 20))
        self._relative_button.setCheckable(True)
        self._relative_button.setIconSize(QtCore.QSize(20, 20))
        self._relative_button.setIcon(QtGui.QIcon(":/icons/light/references.svg"))
        # self._relative_button.setAutoRaise(True)
        self._relative_button.setStyleSheet(CHECK_TOOLBUTTON_STYLESHEET)
        self._relative_button.toggled.connect(self._handle_relative_toggle)
        self._relative_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self._relative_button.setCursor(QtCore.Qt.PointingHandCursor)        
        return self._relative_button

    def _setup_info_button(self):
        self._info = QtWidgets.QPushButton()
        self._info.setMinimumSize(QtCore.QSize(20, 20))
        self._info.setMaximumSize(QtCore.QSize(20, 20))
        # self._info.setCheckable(True)
        self._info.setIconSize(QtCore.QSize(20, 20))
        self._info.setStyleSheet(CHECK_TOOLBUTTON_STYLESHEET)
        self._info.setIcon(QtGui.QIcon(":/icons/light/info.svg"))
        self._info.setFocusPolicy(QtCore.Qt.NoFocus)
        self._info.setCursor(QtCore.Qt.PointingHandCursor)       
        self._info.clicked.connect(self.show_description)
        # self._info.setAutoRaise(True)
        return self._info

    def _setup_enable_button(self):
        self._enabled_button = QtWidgets.QPushButton()
        self._enabled_button.setMinimumSize(QtCore.QSize(35, 25))
        self._enabled_button.setMaximumSize(QtCore.QSize(35, 25))
        self._enabled_button.setCheckable(True)
        self._enabled_button.setIconSize(QtCore.QSize(34, 25))
        self._enabled_button.setIcon(QtGui.QIcon(":/icons/off.png"))
        # self._enabled_button.setAutoRaise(True)       
        self._enabled_button.setStyleSheet(CHECK_TOOLBUTTON_STYLESHEET)
        self._enabled_button.toggled.connect(self._handle_enabled_toggle)
        self._enabled_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self._enabled_button.setCursor(QtCore.Qt.PointingHandCursor)
        return self._enabled_button

    def show_description(self):
        description_label = QtWidgets.QMessageBox()
        description_label.setText("Description")
        description_label.setInformativeText(self.DESCRIPTION)
        description_label.exec_()

    def _handle_enabled_toggle(self, value, force=False):
        icon = QtGui.QIcon(":/icons/off.png") if not value else QtGui.QIcon(":/icons/on.png")
        self._enabled_button.setIcon(icon)
        self._enabled = value

        if force and value:
            self._enabled_button.setChecked(True)

    def _handle_relative_toggle(self, value, force=False):
        icon =  QtGui.QIcon(":/icons/light/references.svg") if not value else QtGui.QIcon(":/icons/references_pushed.png")
        self._relative_button.setIcon(icon)
        self._relative = value

        if force and value:
            self._relative_button.setChecked(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wh = BaseOption()
    # wh.start()
    wh.show()
    app.exec_()


