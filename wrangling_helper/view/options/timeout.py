from gui_utils.Qt import QtWidgets
from wrangling.view.option_widget import BaseOption
from core.utils import time_to_seconds, seconds_to_time


class TimeoutOption(BaseOption):

    NAME = "Timeout"
    DESCRIPTION = "Timeout of the job"
    RELATIVE = True
    DEPENDANT = None        

    def __init__(self, parent=None):
        super(TimeoutOption, self).__init__(parent=parent)

    def setup_option_widget(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        self.hour_spinbox = QtWidgets.QSpinBox()
        self.hour_spinbox.setMinimum(-99)
        self.hour_spinbox.setMaximum(99)
        self.hour_spinbox.setValue(3)
        self.hour_spinbox.setSuffix(" hours")

        self.minute_spinbox = QtWidgets.QSpinBox()
        self.minute_spinbox.setMinimum(-59)
        self.minute_spinbox.setMaximum(59)
        self.minute_spinbox.setValue(30)
        self.minute_spinbox.setSuffix(" minutes")

        widget.setLayout(layout)
        layout.addWidget(self.hour_spinbox)
        layout.addWidget(self.minute_spinbox)
        return widget

    def option_value(self):
        """Method that returns the Value of the option_widget
        
        Returns:
            Any: Depends of the widget
        """
        hours = self.hour_spinbox.value()
        minutes = self.minute_spinbox.value()
        timeout = time_to_seconds(hour=hours, minutes=minutes)
        return timeout

    def option_info(self, job=None):
        if not self.enabled:
            return None

        if self.relative and not job:
            raise Exception()

        options = {"Props":{}}
        value = self.option_value()
        if self.relative:
            timeout = job["Props"]["MaxTime"]
            value = timeout + value

        options["Props"]["MaxTime"] = value
        return options        

    def set_option_value(self, value):
        hour, min = seconds_to_time(value)
        self.hour_spinbox.setValue(int(hour))
        self.minute_spinbox.setValue(int(min))


