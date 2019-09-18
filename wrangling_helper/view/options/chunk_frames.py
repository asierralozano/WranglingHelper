from wrangling.view.options_types.spinbox import SpinBoxOption


class ChunkFramesOption(SpinBoxOption):

    NAME = "Chunk Frames"
    DESCRIPTION = "ChunkFrames of the job"
    RELATIVE = True
    DEPENDANT = None    

    def __init__(self, parent=None):
        super(ChunkFramesOption, self).__init__(parent=parent)

    def _setup_ui(self):
        super(ChunkFramesOption, self)._setup_ui()
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
            concurrent_tasks = job["Props"]["Chunk"]
            value = concurrent_tasks + value

        options["Props"]["Chunk"] = value
        return options