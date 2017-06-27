# import dcc_qc.validators.hathi_lab_factory
import abc

from dcc_qc.checkers import hathi_lab_factory
from dcc_qc import checkers
from dcc_qc.process import AbsProcess, AbsProcessInput, AbsProcessorResults

def add_suite(cls):
    class Wrapper:
        def __init__(self, suite_name, *args):
            self.wrapped = cls(*args)
            self.wrapped.suite = suite_name

        def __getattr__(self, item):
            return getattr(self.wrapped, item)

        def set_suite(self, name):
            self.wrapped.suite = name

    return Wrapper

@add_suite
class PackagePreservationComplete(AbsProcess, AbsProcessInput, AbsProcessorResults):
    def setup(self):
        suite = checkers.get_check_suite(self.suite)
        self.validator = suite.preservation_checkers().completeness_checker()
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

@add_suite
class PackageAccessComplete(AbsProcess, AbsProcessInput, AbsProcessorResults):
    def setup(self):
        suite = checkers.get_check_suite(self.suite)
        self.validator = suite.access_checkers().completeness_checker()
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

@add_suite
class PreservationFileNaming(AbsProcess, AbsProcessInput, AbsProcessorResults):
    def setup(self):
        suite = checkers.get_check_suite(self.suite)
        self.validator = suite.preservation_checkers().naming_checker()
        self._result = None
        self._filename = None

    def run(self):
        self._result = self.validator.check(self._filename)

    @property
    def result(self) -> checkers.Results:
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

@add_suite
class AccessFileNaming(AbsProcess, AbsProcessInput, AbsProcessorResults):
    def setup(self):
        suite = checkers.get_check_suite(self.suite)

        self.validator = suite.access_checkers().naming_checker()
        self._result = None
        self._filename = None

    def set_input(self, value):
        self._filename = value

    @property
    def name(self):
        return "Access file name test"

    @property
    def result(self) -> checkers.Results:
        return self._result

    def run(self):
        self._result = self.validator.check(self._filename)

    @property
    def errors(self):
        return self._result.errors

    def __str__(self):
        return "{}: {}".format(self.name, self._filename)

@add_suite
class PackageStructureComplete(AbsProcess, AbsProcessInput, AbsProcessorResults):
    """Validate the existence of all required folders"""

    def setup(self):
        suite = checkers.get_check_suite(self.suite)
        self.validator = suite.package_checkers().structure_complete_checker()
        self._result = None
        self._path = None

    def run(self):
        result = self.validator.check(self._path)
        self._result = result

    @property
    def errors(self):
        return self._result.errors

    @property
    def result(self) -> checkers.Results:
        return self._result

    @property
    def name(self):
        return "Package Structure Completeness test"

    def set_input(self, value):
        self._path = value

    def __str__(self):
        return "{}: {}".format(self.name, self._path)

@add_suite
class PackageComponentComplete(AbsProcess, AbsProcessInput, AbsProcessorResults):
    """Validate the folders are valid when compared to each other"""

    def setup(self):
        suite = checkers.get_check_suite(self.suite)
        factory = hathi_lab_factory
        self.validator = suite.package_checkers().component_complete_checker()
        self._result = None
        self._path = None

    def run(self):
        result = self.validator.check(self._path)
        self._result = result

    @property
    def errors(self):
        return self._result.errors

    @property
    def result(self) -> checkers.Results:
        return self._result

    @property
    def name(self):
        return "Package Component Completeness test"

    def set_input(self, value):
        self._path = value

    def __str__(self):
        return "{}: {}".format(self.name, self._path)


