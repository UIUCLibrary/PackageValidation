from dcc_qc.task_states.abs_state import AbsTask
from dcc_qc.task_states.statuses import TaskStatus


class TaskEmpty(AbsTask):
    def reset(self):
        pass

    def add_process(self, p):
        self._context.processes.append(p)
        self._context._state = self._context.valid_states["queued"]

    def run(self):
        raise Exception("Nothing to do")

    @property
    def status(self):
        return TaskStatus.EMPTY