from wrangling.view.options_types.combobox import ComboBoxOption
from core.deadline_bootstrap import DeadlineConnection


class PoolOption(ComboBoxOption):

    NAME = "Pool"
    DESCRIPTION = "Pool of the job"
    RELATIVE = False
    DEPENDANT = None    

    def __init__(self, parent=None):
        super(PoolOption, self).__init__(parent=parent)

    def _setup_ui(self):
        super(PoolOption, self)._setup_ui()
        connection = DeadlineConnection()
        pools = connection.get_pools()
        self.option_widget.addItems(pools)        
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
        options["Props"]["Pool"] = value
        return options

