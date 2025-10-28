from dcc_qc.validator.validator import HathiLabValidator
from .profile import AbsProfile
import os
from dcc_qc import tasks, packages
from dcc_qc import validation_processors
from dcc_qc.packages import abs_package

class HathiLab(AbsProfile):
    profile_name = "HathiLab"

    def create_validate_package_task(self, package)->tasks.Task:
        validator = HathiLabValidator()
        my_task = validator.get_validation_task(package)
        return my_task

    @property
    def get_package_type(self) -> abs_package.AbsPackage:
        x = packages.create_package("Hathi")
        return x

