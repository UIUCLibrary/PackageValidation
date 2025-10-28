import abc


class AbsTask(metaclass=abc.ABCMeta):
    def __init__(self, context):
        self._context = context

    @property
    @abc.abstractmethod
    def status(self):
        pass

    @abc.abstractmethod
    def add_process(self, p):
        pass

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def reset(self):
        pass