from dcc_qc.packages import abs_package
import typing
import os
import itertools


class HathiPackage(abs_package.AbsPackage):
    @property
    def items(self) -> typing.Generator[abs_package.PackageItem, None, None]:
        for i in self._items:
            yield i


    def load(self):
        def get_package_paths(path) -> typing.Tuple[str, str]:
            found_access = []
            found_preservation = []

            for root, dirs, files in os.walk(path):
                for dir_ in dirs:
                    if dir_ == "preservation":
                        found_preservation.append(os.path.join(root, dir_))
                    elif dir_ == "access":
                        found_access.append(os.path.join(root, dir_))

            if len(found_access) == 1 and len(found_preservation) == 1:
                return found_access[0], found_preservation[0]

            if len(found_access) > 1 or len(found_preservation) > 1:
                raise Exception("Error: Found multiple access or preservation folders in {}".format(path))

            if len(found_access) == 0 or len(found_preservation) == 0:
                raise Exception("Error: Missing access or preservation folders in {}".format(path))
            raise Exception("Error: Unable to find access and preservation folders in {}".format(path))

        def create_pairs(access_path, preservation_path) -> typing.Generator[typing.Tuple[str, str], None, None]:
            access_folders = [it.path for it in os.scandir(access_path)]
            preservation_folders = [it.path for it in os.scandir(preservation_path)]
            assert len(access_folders) == len(preservation_folders)
            combined = sorted(access_folders + preservation_folders, key=lambda it: str(it.split(os.path.sep)[-1]))
            groups = itertools.groupby(combined, key=lambda it: str(it.split(os.path.sep)[-1]))
            for group, items in groups:
                new_access = None
                new_preservation = None
                for i in items:
                    if i.split(os.path.sep)[-2] == "preservation":
                        new_preservation = i
                    elif i.split(os.path.sep)[-2] == "access":
                        new_access = i
                if new_access is not None and new_preservation is not None:
                    yield new_access, new_preservation
                else:
                    raise Exception("Failed to match preservation folder with an access folder")

        access_path, preservation_path = get_package_paths(self.root_path)
        assert access_path.replace("access", "") == preservation_path.replace("preservation", "")

        for access, preservation in create_pairs(access_path, preservation_path):
            self._items.append(
                abs_package.PackageItem(
                    root=self.root_path,
                    directories={
                        "access": access,
                        "preservation": preservation
                    }
                )
            )
