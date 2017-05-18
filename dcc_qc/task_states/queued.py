from dcc_qc import process
from dcc_qc.task_states.abs_state import AbsTask
from dcc_qc.task_states.statuses import TaskStatus


class TaskQueued(AbsTask):
    def reset(self):
        self._context.processes = []
        self._context._state = self._context.empty

    def add_process(self, p):
        self._context.processes.append(p)

    def run(self):
        self._context._state = self._context.working
        for p in self._context.processes:
            p.run()

            for error in p.errors:
                self._context._errors.append(error)

            if isinstance(p, process.AbsProcessorResults):
                self._context._results.append(p.result)

            if self._context._errors:
                self._context._state = self._context.failed
            else:
                self._context._state = self._context.success

    @property
    def status(self):
        return TaskStatus.QUEUED