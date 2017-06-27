from .profile import AbsProfile
import os
from dcc_qc import tasks, packages
from dcc_qc import validation_processors
from dcc_qc.validator.validator import HathiSubmitValidator
from dcc_qc.packages import abs_package


class HathiSubmit(AbsProfile):
    profile_name = "HathiSubmit"

    @property
    def get_package_type(self) -> abs_package.AbsPackage:
        x = packages.create_package("HathiSubmit")
        return x

    def create_validate_package_task(self, package):
        package_validator = HathiSubmitValidator()
        my_task = package_validator.get_validation_task(package)
        return my_task
