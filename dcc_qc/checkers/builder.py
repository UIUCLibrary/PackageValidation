import abc

from . import abs_checkers, hathi_lab_factory


class Checkers:
    def __init__(self, name):
        self.name = name
        self.access_checker = None
        self.preservation_checker = None
        self.package_checker = None




class AbsBuilder(metaclass=abc.ABCMeta):
    def create_new(self):
        pass

    @abc.abstractmethod
    def create_access_checkers(self) -> abs_checkers.AbsComponentTesterFactory:
        pass

    @abc.abstractmethod
    def create_preservation_checkers(self) -> abs_checkers.AbsComponentTesterFactory:
        pass

    @abc.abstractmethod
    def create_package_checkers(self) -> abs_checkers.AbsPackageFactory:
        pass

    @abc.abstractmethod
    def get_checker(self)->Checkers:
        pass


class HathiLabBuilder(AbsBuilder):

    def create_new(self):
        return Checkers("HathiLab")

    def create_preservation_checkers(self) -> abs_checkers.AbsComponentTesterFactory:
        return hathi_lab_factory.PreservationCheckers()

    def create_access_checkers(self) -> abs_checkers.AbsComponentTesterFactory:
        return hathi_lab_factory.PreservationCheckers()

    def create_package_checkers(self) -> abs_checkers.AbsPackageFactory:
        return hathi_lab_factory.PackageCheckers()


class Director:
    def __init__(self, builder: AbsBuilder):
        self.builder = builder

    def construct(self)->Checkers:
        new_checkers = self.builder.create_new()
        new_checkers.access_checker = self.builder.create_access_checkers()
        new_checkers.preservation_checker = self.builder.create_package_checkers()
        new_checkers.package_checker = self.builder.create_preservation_checkers()
        return new_checkers

