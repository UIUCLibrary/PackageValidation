from dcc_qc.task_states.abs_state import AbsTask
from dcc_qc.task_states.statuses import TaskStatus


class _TaskCompleted(AbsTask):
    @property
    def status(self):
        raise NotImplementedError()

    def reset(self):
        self._context.processes = []
        self._context._state = self._context.valid_states["empty"]

    def add_process(self, p):
        raise Exception("Completed tasks cannot be modified")

    def run(self):
        raise Exception("Tasks already completed")


class TaskSuccess(_TaskCompleted):
    @property
    def status(self):
        return TaskStatus.SUCCESS


class TaskFailed(_TaskCompleted):
    @property
    def status(self):
        return TaskStatus.FAILED
