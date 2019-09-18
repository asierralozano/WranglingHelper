from wrangling.view.options_types.spinbox import SpinBoxOption


class PriorityOption(SpinBoxOption):

    NAME = "Priority"
    DESCRIPTION = "Priority of the job"
    RELATIVE = True
    DEPENDANT = None    

    def __init__(self, parent=None):
        super(PriorityOption, self).__init__(parent=parent)

    def _setup_ui(self):
        super(PriorityOption, self)._setup_ui()
        self.option_widget.setMinimum(-100)
        self.option_widget.setMaximum(100)
        self.option_widget.setValue(50)

    def option_info(self, job=None):
        if not self.enabled:
            return None

        if self.relative and not job:
            raise Exception()

        options = {"Props":{}}
        value = self.option_value()
        if self.relative:
            job_priority = job["Props"]["Pri"]
            value = job_priority + value

        options["Props"]["Pri"] = value
        return options


        
