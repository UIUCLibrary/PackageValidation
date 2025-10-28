from dcc_qc import checkers
from dcc_qc.checkers.abs_checkers import AbsComponentTesterFactory, AbsPackageFactory
from . import hathi_submit

class AccessCheckers(AbsComponentTesterFactory):
    @staticmethod
    def metadata_checker():
        return hathi_submit.AccessMetadataChecker()

    @staticmethod
    def technical_checker():
        return hathi_submit.AccessTechnicalChecker()

    @staticmethod
    def completeness_checker():
        return hathi_submit.AccessCompletenessChecker()

    @staticmethod
    def naming_checker():
        return hathi_submit.AccessNamingChecker()


class PreservationCheckers(AbsComponentTesterFactory):
    @staticmethod
    def metadata_checker():
        return hathi_submit.PresMetadataChecker()

    @staticmethod
    def technical_checker():
        return hathi_submit.PresTechnicalChecker()

    @staticmethod
    def completeness_checker():
        return hathi_submit.PresCompletenessChecker()

    @staticmethod
    def naming_checker():
        return hathi_submit.PresNamingChecker()


class PackageCheckers(AbsPackageFactory):
    @staticmethod
    def structure_complete_checker():
        return hathi_submit.PackageStructureChecker()

    @staticmethod
    def component_complete_checker():
        return hathi_submit.PackageComponentChecker()
