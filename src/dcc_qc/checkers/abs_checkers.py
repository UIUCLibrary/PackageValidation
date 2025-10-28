import abc


class AbsComponentTesterFactory(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def technical_checker():
        pass

    @staticmethod
    @abc.abstractmethod
    def metadata_checker():
        pass

    @staticmethod
    @abc.abstractmethod
    def completeness_checker():
        pass

    @staticmethod
    @abc.abstractmethod
    def naming_checker():
        pass


class AbsPackageFactory(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def structure_complete_checker():
        pass

    @staticmethod
    @abc.abstractmethod
    def component_complete_checker():
        pass


class AbsChecker(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check(self, path):
        pass

    @staticmethod
    @abc.abstractmethod
    def checker_name():
        pass
