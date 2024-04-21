import abc


class TaskTracker(abc.ABC):
    """Interface class for task trackers"""

    def __init__(self, name: str, *args, **kargs) -> None:
        self._name = name
        # self._boards = []
