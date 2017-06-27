from dcc_qc import checkers
from dcc_qc.checkers.abs_checkers import AbsComponentTesterFactory, AbsPackageFactory


class AccessCheckers(AbsComponentTesterFactory):
    @staticmethod
    def metadata_checker():
        return checkers.hathi_lab.AccessMetadataChecker()

    @staticmethod
    def technical_checker():
        return checkers.hathi_lab.AccessTechnicalChecker()

    @staticmethod
    def completeness_checker():
        return checkers.hathi_lab.AccessCompletenessChecker()

    @staticmethod
    def naming_checker():
        return checkers.hathi_lab.AccessNamingChecker()


class PreservationCheckers(AbsComponentTesterFactory):
    @staticmethod
    def metadata_checker():
        return checkers.hathi_lab.PresMetadataChecker()

    @staticmethod
    def technical_checker():
        return checkers.hathi_lab.PresTechnicalChecker()

    @staticmethod
    def completeness_checker():
        return checkers.hathi_lab.PresCompletenessChecker()

    @staticmethod
    def naming_checker():
        return checkers.hathi_lab.PresNamingChecker()


class PackageCheckers(AbsPackageFactory):
    @staticmethod
    def structure_complete_checker():
        return checkers.hathi_lab.PackageStructureChecker()

    @staticmethod
    def component_complete_checker():
        return checkers.hathi_lab.PackageComponentChecker()
