import abc

from dcc_qc import checkers


class AbsProcess(metaclass=abc.ABCMeta):
    """Implement this abstract class to to use a process with the task manager."""
    def __init__(self):
        self._errors = []
        self._name = ""

    @abc.abstractmethod
    def setup(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass

    @property
    def errors(self):
        return self._errors

    @property
    def name(self):
        return self._name


class AbsProcessInput(metaclass=abc.ABCMeta):
    """Abstract class to be used with AbsProcess. Implement if the process has an input"""
    @abc.abstractmethod
    def set_input(self, value):
        pass


class AbsProcessorResults(metaclass=abc.ABCMeta):
    """Abstract class to be uses with AbsProcess. Implement if the process has a return data"""
    @property
    @abc.abstractmethod
    def result(self)->checkers.Results:
        pass
