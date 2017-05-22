import typing

from dcc_qc.validators import results
from dcc_qc import task_states

from dcc_qc.task_states import statuses


class Task:
    def __init__(self, description="Generic task"):

        # Set the valid  states
        self.valid_states = {
            "queued": task_states.TaskQueued(self),
            "empty": task_states.TaskEmpty(self),
            "working": task_states.TaskWorking(self),
            "success": task_states.TaskSuccess(self),
            "failed": task_states.TaskFailed(self),

        }

        self._name = description
        self._results = []
        self._errors = []
        self._state = self.valid_states["empty"]
        self.processes = []

    def __len__(self):
        return len(self.processes)

    @property
    def results(self) -> typing.List[results.Results]:
        """List of public result produced during the run() method, if any."""
        return self._results

    @property
    def errors(self):
        """List of any errors produced during the run() method, if any."""
        errors = []
        for result in self.results:
            errors += result.errors
        return errors

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