from wrangling.view.options_types.spinbox import SpinBoxOption
from core.utils import get_chunk_frames



class TasksOption(SpinBoxOption):

    NAME = "Tasks"
    DESCRIPTION = "ChunkFrames of the job"
    RELATIVE = False
    DEPENDANT = None    

    def __init__(self, parent=None):
        super(TasksOption, self).__init__(parent=parent)

    def _setup_ui(self):
        super(TasksOption, self)._setup_ui()
        self.option_widget.setMinimum(1)
        self.option_widget.setMaximum(100)
        self.option_widget.setValue(1)

    def option_info(self, job=None):
        if not self.enabled:
            return None

        if self.relative and not job:
            raise Exception()

        options = {"Props":{}}
        value = self.option_value()
        frames = job["Props"]["Frames"]
        chunk_frames = get_chunk_frames(value, frames)
        options["Props"]["Chunk"] = chunk_frames

        return options