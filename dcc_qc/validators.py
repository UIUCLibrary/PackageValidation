import abc


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


class AbsValidator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check(self, file_):
        pass


class AccessValidators(AbsFactory):
    @staticmethod
    def metadata_checker():
        pass

    @staticmethod
    def technical_checker():
        pass

    @staticmethod
    def completeness_checker():
        pass

    @staticmethod
    def naming_checker():
        pass


class PreservationValidators(AbsFactory):
    @staticmethod
    def metadata_checker():
        return PresMetadataChecker()

    @staticmethod
    def technical_checker():
        return PresTechnicalChecker()

    @staticmethod
    def completeness_checker():
        return PresCompletenessChecker()

    @staticmethod
    def naming_checker():
        return PresNamingChecker()


# =================
# Concrete Classes
# =================


class Result:
    # TODO: Create Result() class

    @property
    def valid(self):
        return False

    @property
    def errors(self)->list:
        return []


class PresCompletenessChecker(AbsValidator):
    # TODO: Create PresCompletenessChecker() class
    def check(self, file):
        pass


class PresNamingChecker(AbsValidator):
    # TODO: Create PresNamingChecker() class
    def check(self, file):
        pass


class PresMetadataChecker(AbsValidator):
    # TODO: Create PresMetadataChecker() class
    def check(self, file):
        pass


class PresTechnicalChecker(AbsValidator):
    # TODO: Create PresTechnicalChecker() class
    def check(self, file):
        pass


class AccessCompletenessChecker(AbsValidator):
    # TODO: Create AccessCompletenessChecker() class
    def check(self, file):
        pass


class AccessNamingChecker(AbsValidator):
    # TODO: Create AccessNamingChecker() class
    def check(self, file):
        pass


class AccessMetadataChecker(AbsValidator):
    # TODO: Create AccessMetadataChecker() class
    def check(self, file):
        pass


class AccessTechnicalChecker(AbsValidator):
    # TODO: Create AccessTechnicalChecker() class
    def check(self, file):
        pass
