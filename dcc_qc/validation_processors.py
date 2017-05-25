# import dcc_qc.validators.hathi_lab_factory
from dcc_qc.validators import hathi_lab_factory
from dcc_qc import validators
from dcc_qc.process import AbsProcess, AbsProcessInput, AbsProcessorResults


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

    def __str__(self):
        return "{}: {}".format(self.name, self._path)


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

    def __str__(self):
        return "{}: {}".format(self.name, self._path)

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

    def __str__(self):
        return "{}: {}".format(self.name, self._filename)


class AccessFileNaming(AbsProcess, AbsProcessInput, AbsProcessorResults):
    def setup(self):
        self.valitator = hathi_lab_factory.AccessValidators.naming_checker()
        self._result = None
        self._filename = None

    def set_input(self, value):
        self._filename = value

    @property
    def name(self):
        return "Access file name test"

    @property
    def result(self) -> validators.Results:
        return self._result

    def run(self):
        self._result = self.valitator.check(self._filename)

    @property
    def errors(self):
        return self._result.errors

    def __str__(self):
        return "{}: {}".format(self.name, self._filename)


class PackageStructureComplete(AbsProcess, AbsProcessInput, AbsProcessorResults):
    """Validate the existence of all required folders"""

    def setup(self):
        self.validator = hathi_lab_factory.PackageValidators.structure_complete_checker()
        self._result = None
        self._path = None

    def run(self):
        result = self.validator.check(self._path)
        self._result = result

    @property
    def errors(self):
        return self._result.errors

    @property
    def result(self) -> validators.Results:
        return self._result

    @property
    def name(self):
        return "Package Structure Completeness test"

    def set_input(self, value):
        self._path = value

    def __str__(self):
        return "{}: {}".format(self.name, self._path)


class PackageComponentComplete(AbsProcess, AbsProcessInput, AbsProcessorResults):
    """Validate the folders are valid when compared to each other"""

    def setup(self):
        self.validator = hathi_lab_factory.PackageValidators.component_complete_checker()
        self._result = None
        self._path = None

    def run(self):
        result = self.validator.check(self._path)
        self._result = result

    @property
    def errors(self):
        return self._result.errors

    @property
    def result(self) -> validators.Results:
        return self._result

    @property
    def name(self):
        return "Package Component Completeness test"

    def set_input(self, value):
        self._path = value

    def __str__(self):
        return "{}: {}".format(self.name, self._path)
