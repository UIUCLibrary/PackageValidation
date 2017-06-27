import abc
import os
from dcc_qc import tasks, validation_processors


class AbsValidator(metaclass=abc.ABCMeta):
    """Set what validations are needed for a given package"""

    @abc.abstractmethod
    def get_validation_task(self, package) -> tasks.Task:
        pass


class HathiSubmitValidator(AbsValidator):
    def get_validation_task(self, package) -> tasks.Task:
        task_name = package.directories["access"].split(os.path.sep)[-1]

        my_task = tasks.Task(description="Validating {} in {}".format(task_name, package.root))

        # Package Structure Completeness:
        my_task.add_process(self.package_structure(package))

        # Package component Completeness:
        # my_task.add_process(self.package_component(package))

        # Access folder
        # my_task.add_process(self.access_folder_completeness(package))

        # Access file name
        for file in os.scandir(package.directories["access"]):
            access_file_naming_test = self.access_file_naming(file)
            my_task.add_process(access_file_naming_test)
        return my_task

    @staticmethod
    def access_file_naming(file):
        access_file_naming_test = validation_processors.AccessFileNaming()
        access_file_naming_test.setup()
        access_file_naming_test.set_input(file.path)
        return access_file_naming_test

    @staticmethod
    def access_folder_completeness(package):
        access_folder_completeness_test = validation_processors.PackageAccessComplete()
        access_folder_completeness_test.setup()
        access_folder_completeness_test.set_input(package.directories['access'])
        return access_folder_completeness_test

    @staticmethod
    def package_component(package):
        package_component_test = validation_processors.PackageComponentComplete()
        package_component_test.setup()
        package_component_test.set_input(package)
        return package_component_test

    @staticmethod
    def package_structure(package):
        package_structure_test = validation_processors.PackageStructureComplete()
        package_structure_test.setup()
        package_structure_test.set_input(package.root)
        return package_structure_test


class HathiLabValidator(AbsValidator):
    def get_validation_task(self, package) -> tasks.Task:

        task_name = package.directories["preservation"].split(os.path.sep)[-1]

        my_task = tasks.Task(description="Validating {} in {}".format(task_name, package.root))

        # Package Structure Completeness:
        my_task.add_process(self.package_structure(package))

        # Package component Completeness:
        my_task.add_process(self.package_component(package))

        # Preservation Folder
        my_task.add_process(self.preservation_folder(package))

        # Access folder
        my_task.add_process(self.access_folder_completeness(package))

        # Preservation file name
        for file in os.scandir(package.directories["preservation"]):
            my_task.add_process(self.preservation_file_naming(file))

        # Access file name
        for file in os.scandir(package.directories["access"]):
            my_task.add_process(self.access_file_naming(file))
        return my_task


    def access_file_naming(self, file):
        access_file_naming_test = validation_processors.AccessFileNaming()
        access_file_naming_test.setup()
        access_file_naming_test.set_input(file.path)
        return access_file_naming_test

    @staticmethod
    def preservation_file_naming(file):
        preservation_file_naming_test = validation_processors.PreservationFileNaming()
        preservation_file_naming_test.setup()
        preservation_file_naming_test.set_input(file.path)
        return preservation_file_naming_test

    @staticmethod
    def access_folder_completeness(package):
        access_folder_completeness_test = validation_processors.PackageAccessComplete()
        access_folder_completeness_test.setup()
        access_folder_completeness_test.set_input(package.directories['access'])
        return access_folder_completeness_test

    @staticmethod
    def preservation_folder(package):
        preservation_folder_completeness_test = validation_processors.PackagePreservationComplete()
        preservation_folder_completeness_test.setup()
        preservation_folder_completeness_test.set_input(package.directories["preservation"])
        return preservation_folder_completeness_test

    @staticmethod
    def package_component(package):
        package_component_test = validation_processors.PackageComponentComplete()
        package_component_test.setup()
        package_component_test.set_input(package)
        return package_component_test

    @staticmethod
    def package_structure(package):
        package_structure_test = validation_processors.PackageStructureComplete()
        package_structure_test.setup()
        package_structure_test.set_input(package.root)
        return package_structure_test
