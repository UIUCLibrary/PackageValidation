import abc

import sys

from . import abs_checkers
from . import hathi_lab_factory, hathi_submit_factory
from inspect import getmembers, isclass, isabstract


class AbsCheckSuite(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def preservation_checkers() -> abs_checkers.AbsComponentTesterFactory:
        pass

    @staticmethod
    @abc.abstractmethod
    def access_checkers() -> abs_checkers.AbsComponentTesterFactory:
        pass

    @staticmethod
    @abc.abstractmethod
    def package_checkers() -> abs_checkers.AbsPackageFactory:
        pass


class HathiLab(AbsCheckSuite):
    @staticmethod
    def access_checkers() -> abs_checkers.AbsComponentTesterFactory:
        return hathi_lab_factory.AccessCheckers()

    @staticmethod
    def preservation_checkers() -> abs_checkers.AbsComponentTesterFactory:
        return hathi_lab_factory.PreservationCheckers()

    @staticmethod
    def package_checkers() -> abs_checkers.AbsPackageFactory:
        return hathi_lab_factory.PackageCheckers()


class HathiSubmit(AbsCheckSuite):
    @staticmethod
    def access_checkers() -> abs_checkers.AbsComponentTesterFactory:
        return hathi_submit_factory.AccessCheckers()

    @staticmethod
    def preservation_checkers() -> abs_checkers.AbsComponentTesterFactory:
        return hathi_submit_factory.PreservationCheckers()

    @staticmethod
    def package_checkers() -> abs_checkers.AbsPackageFactory:
        return hathi_submit_factory.PackageCheckers()


class Null(AbsCheckSuite):
    @staticmethod
    def access_checkers() -> abs_checkers.AbsComponentTesterFactory:
        raise NotImplementedError()

    @staticmethod
    def preservation_checkers() -> abs_checkers.AbsComponentTesterFactory:
        raise NotImplementedError()

    @staticmethod
    def package_checkers() -> abs_checkers.AbsPackageFactory:
        raise NotImplementedError()


class CheckSuiteFactory:
    suits = {}

    def __init__(self):
        self.load_suites()

    def load_suites(self):
        classes = getmembers(sys.modules[__name__], lambda s: isclass(s) and not isabstract(s))
        for name, _type in classes:
            if isclass(_type) and issubclass(_type, AbsCheckSuite):
                self.suits.update([[name, _type]])

    def create_instance(self, suite_name):
        return self.suits[suite_name]()
        # if suite_name in self.suits:
        #     pass
        # else:
        # # return self.suits["Null"]()