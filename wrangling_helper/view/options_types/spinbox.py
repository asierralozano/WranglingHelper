from gui_utils.Qt import QtWidgets
from ..option_widget import BaseOption
from ...resources import resource


STYLESHEET = """
    QSpinBox{
        border:1px solid lightgrey; 
        border-radius: 4px
    }

    QSpinBox::up-button {
        background:transparent;
    }

    QSpinBox::up-arrow {
        image: url(:/icons/light/chevron-up.svg);
        width: 7px;
        height: 7px;
    }

    QSpinBox::down-button {
        background:transparent;
    }

    QSpinBox::down-arrow {
        image: url(:/icons/light/chevron-down.svg);
        width: 7px;
        height: 7px;
    }
"""

class SpinBoxOption(BaseOption):

    def __init__(self, parent=None):
        super(SpinBoxOption, self).__init__(parent=parent)

    def setup_option_widget(self):
        spinbox = QtWidgets.QSpinBox()
        # spinbox.setStyleSheet(STYLESHEET)
        return spinbox

    def option_value(self):
        """Method that returns the Value of the option_widget
        
        Returns:
            Any: Depends of the widget
        """
        return self.option_widget.value()

    def set_option_value(self, value):
        self.option_widget.setValue(value)

