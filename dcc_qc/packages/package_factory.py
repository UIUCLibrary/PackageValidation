from inspect import getmembers, isclass, isabstract
from dcc_qc import packages


class PackageFactory:
    packages = {}

    def __init__(self):
        self.load_packages()

    def load_packages(self):

        classes = getmembers(packages, lambda m: isclass(m) and not isabstract(m))
        for name, _type in classes:
            if isclass(_type) and issubclass(_type, packages.abs_package.AbsPackage):
                self.packages.update([[name, _type]])

    def create_instance(self, package_name, root):
        return self.packages[package_name](root)