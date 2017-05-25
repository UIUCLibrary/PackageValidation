from dcc_qc import validators
from dcc_qc.validators.abs_validators import AbsComponentTesterFactory, AbsPackageFactory


class AccessValidators(AbsComponentTesterFactory):
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


class PreservationValidators(AbsComponentTesterFactory):
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


class PackageValidators(AbsPackageFactory):
    @staticmethod
    def structure_complete_checker():
        return validators.hathi_lab.PackageStructureChecker()

    @staticmethod
    def component_complete_checker():
        return validators.hathi_lab.PackageComponentChecker()
