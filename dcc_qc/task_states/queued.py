from dcc_qc.task_states.abs_state import AbsTask
from dcc_qc.task_states.statuses import TaskStatus


class TaskQueued(AbsTask):
    def reset(self):
        self._context.processes = []
        self._context._state = self._context.valid_states["empty"]

    def add_process(self, p):
        self._context.processes.append(p)

    def run(self):
        self._context._state = self._context.valid_states["working"]
        status = self._context.valid_states["success"]
        for p in self._context.processes:
            self._context._run_process(process_to_run=p)
            if self._context._errors or not p.result.valid:
                status = self._context.valid_states["failed"]

        self._context._state = status

    @property
    def status(self):
        return TaskStatus.QUEUED
