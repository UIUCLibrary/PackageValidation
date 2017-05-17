from dcc_qc import validators
from dcc_qc.process import AbsProcess, AbsProcessInput, AbsProcessorResults


class PackagePreservationComplete(AbsProcess, AbsProcessInput, AbsProcessorResults):
    def setup(self):
        self.validator = validators.PreservationValidators().completeness_checker()
        self._path = None
        self._result = None

    def run(self):
        assert self._path, "Did you use set_up() method to set a path?"
        self._result = self.validator.check(self._path)

    def set_input(self, value):
        self._path = value

    @property
    def result(self):
        return self._result
