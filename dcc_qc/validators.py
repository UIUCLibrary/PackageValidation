import abc

from dcc_qc import checkers


class AbsFactory(metaclass=abc.ABCMeta):
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


class AccessValidators(AbsFactory):
    @staticmethod
    def metadata_checker():
        return checkers.AccessMetadataChecker

    @staticmethod
    def technical_checker():
        return checkers.AccessTechnicalChecker

    @staticmethod
    def completeness_checker():
        return checkers.AccessCompletenessChecker

    @staticmethod
    def naming_checker():
        return checkers.AccessNamingChecker()


class PreservationValidators(AbsFactory):
    @staticmethod
    def metadata_checker():
        return checkers.PresMetadataChecker()

    @staticmethod
    def technical_checker():
        return checkers.PresTechnicalChecker()

    @staticmethod
    def completeness_checker():
        return checkers.PresCompletenessChecker()

    @staticmethod
    def naming_checker():
        return checkers.PresNamingChecker()
