import abc

from dcc_qc import validators


class AbsProcess(metaclass=abc.ABCMeta):
    """Implement this abstract class to to use a process with the task manager."""

    @abc.abstractmethod
    def setup(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass

    @property
    @abc.abstractmethod
    def errors(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        pass


class AbsProcessInput(metaclass=abc.ABCMeta):
    """Abstract class to be used with AbsProcess. Implement if the process has an input"""

    @abc.abstractmethod
    def set_input(self, value):
        pass


class AbsProcessorResults(metaclass=abc.ABCMeta):
    """Abstract class to be uses with AbsProcess. Implement if the process has a return data"""

    @property
    @abc.abstractmethod
    def result(self) -> validators.Results:
        pass
