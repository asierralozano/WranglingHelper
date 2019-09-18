from .priority import PriorityOption
from .machine_limit import MachineLimitOption
from .concurrent_tasks import ConcurrentTasksOption
from .chunk_frames import ChunkFramesOption
from .tasks import TasksOption
from .timeout import TimeoutOption
from .group import GroupOption
from .pool import PoolOption

OPTIONS = [
    PriorityOption,
    MachineLimitOption,
    ConcurrentTasksOption,
    ChunkFramesOption,
    TasksOption,
    TimeoutOption,
    GroupOption,
    PoolOption
]