import typing

from dcc_qc import checkers
from dcc_qc import task_states

from dcc_qc.task_states import statuses


class Task:
    def __init__(self, name="Generic task"):

        # Set the valid  states
        self.queued = task_states.TaskQueued(self)
        self.empty = task_states.TaskEmpty(self)
        self.working = task_states.TaskWorking(self)
        self.success = task_states.TaskSuccess(self)
        self.failure = task_states.TaskFailed(self)

        self._name = name
        self._results = []
        self._errors = []
        self._state = self.empty
        self.processes = []

    def __len__(self):
        return len(self.processes)

    @property
    def results(self) -> typing.List[checkers.Results]:
        """List of public results produced during the run() method, if any."""
        return self._results

    @property
    def errors(self):
        """List of any errors produced during the run() method, if any."""
        return self._errors

    @property
    def name(self):
        """Short and human-readable result_type explaining what the task does."""
        return self._name

    @property
    def status(self) -> statuses.TaskStatus:
        return self._state.status

    def run(self):
        self._state.run()

    def add_process(self, p):
        self._state.add_process(p)

    def reset(self):
        self._state.reset()