import abc
from dcc_qc.packages import abs_package

class AbsProfile(metaclass=abc.ABCMeta):
    profile_name = "abstract profile"

    @abc.abstractmethod
    def create_validate_package_task(self, package):
        pass

    @property
    @abc.abstractmethod
    def get_package_type(self)->abs_package.AbsPackage:
        pass