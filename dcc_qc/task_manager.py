from collections import abc
from enum import Enum
import typing
from dcc_qc import checkers
from dcc_qc import process


class TaskStatus(Enum):
    QUEUED = "queued"
    WORKING = "working"
    FAILED = "failed"
    SUCCESS = "success"


class Task:
    """The Task class contains all the processes need to run by the TaskManager class"""

    def __init__(self, name="Generic task"):
        self._processes = []
        self._name = name
        self._results = []
        self._errors = []
        self.status = TaskStatus.QUEUED

    def add_process(self, p):
        self._processes.append(p)

    def run(self):
        self.status = TaskStatus.WORKING

        for p in self._processes:
            p.run()
            for error in p.errors:
                self._errors.append(error)

            if isinstance(p, process.AbsProcessorResults):
                self._results.append(p.result)

        if self._errors:
            self.status = TaskStatus.FAILED
        else:
            self.status = TaskStatus.SUCCESS

    @property
    def name(self):
        """Short and human-readable result_type explaining what the task does."""
        return self._name

    @property
    def results(self) -> typing.List[checkers.Results]:
        """List of public results produced during the run() method, if any."""
        return self._results

    @property
    def errors(self):
        """List of any errors produced during the run() method, if any."""
        return self._errors


class TaskManager(abc.Collection):
    def __init__(self):
        self._processes = []

    def __contains__(self, x):
        for p in self._processes:
            if p.result_type == x:
                return True
        return False

    def __len__(self):
        return len(self._processes)

    def __iter__(self) -> process.AbsProcess:
        for p in self._processes:
            yield p

    def push_task(self, task: Task):
        self._processes.append(task)
