import collections
import typing

from dcc_qc import process
from dcc_qc.tasks import Task


class TaskManager(collections.abc.MutableSequence):
    def __init__(self):
        self._processes = []

    def __contains__(self, x):
        for p in self._processes:
            if p.result_type == x:
                return True
        return False

    def __len__(self):
        return len(self._processes)

    def __iter__(self) -> typing.Iterable[process.AbsProcess]:
        for p in self._processes:
            yield p

    def __getitem__(self, index):
        return self._processes[index]

    def __delitem__(self, index):
        del self._processes[index]

    def __setitem__(self, index, value):
        self._processes[index] = value

    def insert(self, index, value):
        self._processes.insert(index, value)

    def push(self, task: Task):
        self._processes.append(task)
