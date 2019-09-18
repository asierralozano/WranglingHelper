from gui_utils.Qt import QtWidgets
from ..option_widget import BaseOption


class ComboBoxOption(BaseOption):

    def __init__(self, parent=None):
        super(ComboBoxOption, self).__init__(parent=parent)

    def setup_option_widget(self):
        return QtWidgets.QComboBox()

    def option_value(self):
        """Method that returns the Value of the option_widget
        
        Returns:
            Any: Depends of the widget
        """
        return str(self.option_widget.currentText())

    def set_option_value(self, value):
        index = self.option_widget.findText(value)
        self.option_widget.setCurrentIndex(index)

