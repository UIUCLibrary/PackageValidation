import abc
from dcc_qc import task_manager


class AbsRunner(metaclass=abc.ABCMeta):
    def __init__(self, entry_path):
        self.path = entry_path
        self.errors = []
        self.valid = True
        self.manager = task_manager.TaskManager()
        self.setup()

    @abc.abstractmethod
    def run(self):
        """Execute the commands in the task manager"""
        pass

    @abc.abstractmethod
    def setup(self):
        """Configure and queue of the tasks that need to be run but the task manager"""
        pass
