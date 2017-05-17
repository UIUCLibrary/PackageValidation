from dcc_qc.task_states.abs_state import AbsTask
from dcc_qc.task_states.statuses import TaskStatus


class TaskWorking(AbsTask):
    def reset(self):
        raise RuntimeError("Task in progress")

    def add_process(self, p):
        raise RuntimeError("Task in progress")

    def run(self):
        raise RuntimeError("Task in progress")

    @property
    def status(self):
        return TaskStatus.WORKING