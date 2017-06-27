from dcc_qc.packages.abs_package import AbsPackage, PackageItem
from dcc_qc import packages
import typing
import os
import itertools
from collections import namedtuple

class HathiSubmitPackage(AbsPackage):

    @staticmethod
    def get_packages(path):
        for package_path in filter(lambda x: x.is_dir(),os.scandir(path)):
            yield PackageItem(
                root=path,
                identifier=package_path.name,
                directories={
                    "access": package_path.path,
                }
            )


    def get_package_level_files(self) -> typing.Iterable[PackageItem]:
        #TODO: get_package_level_files
        return super().get_package_level_files()
