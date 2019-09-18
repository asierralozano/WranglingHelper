from wrangling.view.options_types.spinbox import SpinBoxOption


class MachineLimitOption(SpinBoxOption):

    NAME = "Machine Limit"
    DESCRIPTION = "Machine Limit of the job"
    RELATIVE = True
    DEPENDANT = None    

    def __init__(self, parent=None):
        super(MachineLimitOption, self).__init__(parent=parent)

    def _setup_ui(self):
        super(MachineLimitOption, self)._setup_ui()
        self.option_widget.setMinimum(-100)
        self.option_widget.setMaximum(100)
        self.option_widget.setValue(1)

    def option_info(self, job=None):
        if not self.enabled:
            return None

        if self.relative and not job:
            raise Exception()

        options = {"Props":{}}
        value = self.option_value()
        if self.relative:
            machine_limit = job["Props"]["MachLmt"]
            value = machine_limit + value

        options["Props"]["MachLmt"] = value
        return options

