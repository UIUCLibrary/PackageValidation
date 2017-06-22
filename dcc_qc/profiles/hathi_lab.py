from .profile import AbsProfile
import os
from dcc_qc import tasks, packages
from dcc_qc import validation_processors
from dcc_qc.packages import abs_package

class HathiLab(AbsProfile):
    profile_name = "HathiLab"

    def create_validate_package_task(self, package)->tasks.Task:
        task_name = package.directories["preservation"].split(os.path.sep)[-1]

        my_task = tasks.Task(description="Validating {} in {}".format(task_name, package.root))

        # Package Structure Completeness:
        package_structure_test = validation_processors.PackageStructureComplete()
        package_structure_test.setup()
        package_structure_test.set_input(package.root)
        my_task.add_process(package_structure_test)

        # Package component Completeness:
        package_component_test = validation_processors.PackageComponentComplete()
        package_component_test.setup()
        package_component_test.set_input(package)
        my_task.add_process(package_component_test)

        # Preservation Folder
        preservation_folder_completeness_test = validation_processors.PackagePreservationComplete()
        preservation_folder_completeness_test.setup()
        preservation_folder_completeness_test.set_input(package.directories["preservation"])
        my_task.add_process(preservation_folder_completeness_test)

        # Access folder
        access_folder_completeness_test = validation_processors.PackageAccessComplete()
        access_folder_completeness_test.setup()
        access_folder_completeness_test.set_input(package.directories['access'])
        my_task.add_process(access_folder_completeness_test)

        # Preservation file name
        for file in os.scandir(package.directories["preservation"]):
            preservation_file_naming_test = validation_processors.PreservationFileNaming()
            preservation_file_naming_test.setup()
            preservation_file_naming_test.set_input(file.path)
            my_task.add_process(preservation_file_naming_test)

        # Access file name
        for file in os.scandir(package.directories["access"]):
            access_file_naming_test = validation_processors.AccessFileNaming()
            access_file_naming_test.setup()
            access_file_naming_test.set_input(file.path)
            my_task.add_process(access_file_naming_test)

        return my_task

    @property
    def get_package_type(self) -> abs_package.AbsPackage:
        x = packages.create_package("Hathi")
        return x

