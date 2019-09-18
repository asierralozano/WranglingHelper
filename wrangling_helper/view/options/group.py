from wrangling.view.options_types.combobox import ComboBoxOption
from core.deadline_bootstrap import DeadlineConnection


class GroupOption(ComboBoxOption):

    NAME = "Group"
    DESCRIPTION = "Group of the job"
    RELATIVE = False
    DEPENDANT = None    

    def __init__(self, parent=None):
        super(GroupOption, self).__init__(parent=parent)

    def _setup_ui(self):
        super(GroupOption, self)._setup_ui()
        connection = DeadlineConnection()
        groups = connection.get_group_names()
        self.option_widget.addItems(groups)        
        # self.option_widget.setMinimum(-100)
        # self.option_widget.setMaximum(100)
        # self.option_widget.setValue(1)

    def option_info(self, job=None):
        if not self.enabled:
            return None

        if self.relative and not job:
            raise Exception()

        options = {"Props":{}}
        value = self.option_value()
        options["Props"]["Grp"] = value
        return options

