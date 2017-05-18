# import dcc_qc.validators.hathi_lab_factory
from dcc_qc.validators import hathi_lab_factory
from dcc_qc import validators
from dcc_qc.process import AbsProcess, AbsProcessInput, AbsProcessorResults
import functools


class PackagePreservationComplete(AbsProcess, AbsProcessInput, AbsProcessorResults):
    def setup(self):
        self.validator = hathi_lab_factory.PreservationValidators.completeness_checker()
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

    @property
    def name(self):
        return "Preservation folder completeness test"

    @property
    def errors(self):
        return self.result.errors
        # if len(self._result.errors) > 0:
        #     return functools.reduce(lambda lhs, rhs: lhs + rhs, self._result.errors, [])
        # else:
        #     return []



class PackageAccessComplete(AbsProcess, AbsProcessInput, AbsProcessorResults):
    def setup(self):
        self.validator = hathi_lab_factory.AccessValidators.completeness_checker()
        self._path = None
        self._results = None

    def run(self):
        assert self._path, "Did you use set_up() method to set a path?"
        self._result = self.validator.check(self._path)

    def set_input(self, value):
        self._path = value

    @property
    def result(self):
        return self._result

    @property
    def name(self):
        return "Access folder completeness test"

    @property
    def errors(self):
        return self.result.errors
        # if len(self._result.errors) > 0:
        #     return functools.reduce(lambda lhs, rhs: lhs + rhs, self._result, [])
        # else:
        #     return []


class PreservationFileNaming(AbsProcess, AbsProcessInput, AbsProcessorResults):
    def setup(self):
        self.valitator = hathi_lab_factory.PreservationValidators.naming_checker()
        self._result = None
        self._filename = None

    def run(self):
        self._result = self.valitator.check(self._filename)

    @property
    def result(self) -> validators.Results:
        return self._result

    @property
    def name(self):
        return "Preservation file name test"

    def set_input(self, value):
        self._filename = value

    @property
    def errors(self):
        return self.result.errors
        # if len(self._result.errors) > 0:
        #     return functools.reduce(lambda lhs, rhs: lhs + rhs, self._result.errors, [])
        # else:
        #     return []
        # return functools.reduce(lambda lhs, rhs: lhs + rhs, [r.errors for r in self._results], [])
