from dcc_qc import validators
from dcc_qc.validators.abs_validators import AbsFactory


class AccessValidators(AbsFactory):
    @staticmethod
    def metadata_checker():
        return validators.hathi_lab.AccessMetadataChecker()

    @staticmethod
    def technical_checker():
        return validators.hathi_lab.AccessTechnicalChecker()

    @staticmethod
    def completeness_checker():
        return validators.hathi_lab.AccessCompletenessChecker()

    @staticmethod
    def naming_checker():
        return validators.hathi_lab.AccessNamingChecker()


class PreservationValidators(AbsFactory):
    @staticmethod
    def metadata_checker():
        return validators.hathi_lab.PresMetadataChecker()

    @staticmethod
    def technical_checker():
        return validators.hathi_lab.PresTechnicalChecker()

    @staticmethod
    def completeness_checker():
        return validators.hathi_lab.PresCompletenessChecker()

    @staticmethod
    def naming_checker():
        return validators.hathi_lab.PresNamingChecker()