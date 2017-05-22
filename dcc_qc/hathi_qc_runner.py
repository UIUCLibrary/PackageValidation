"""
This will become a script but for now it's just a sample implementation. 
I'm using it to check that my validators work and my package API make 
sense when it is consumed by a script.
"""
import os
import typing
import functools
import warnings
import sys

from dcc_qc import task_manager, tasks, packages
from dcc_qc import validation_processors
from dcc_qc.abs_runner import AbsRunner
from dcc_qc.task_states import TaskStatus


class HathiQCRunner(AbsRunner):
    @staticmethod
    def get_package_folders(path) -> typing.Generator[packages.abs_package.AbsPackage, None, None]:
        with os.scandir(path) as search_path:
            for item in search_path:
                if item.is_dir():
                    yield item.path

    def setup(self):
        self.packages = []

        try:
            package_set = packages.create_package("Hathi", self.path)
            for package in package_set:
                self.packages.append(package)
        except packages.PackageError as e:
            self.valid = False
            self.errors.append("Unable to validate {}. Reason: {}".format(self.path, e))

        # Add the tasks that need to be validated
        for hathi_package in self.packages:
            task_name = hathi_package.directories["preservation"].split(os.path.sep)[-1]

            my_task = tasks.Task(description="Validating {} in {}".format(task_name, hathi_package.root))

            # Package Completeness:
            package_completeness_test = validation_processors.PackageComplete()
            package_completeness_test.setup()
            package_completeness_test.set_input(hathi_package.root)
            my_task.add_process(package_completeness_test)

            # Preservation Folder
            preservation_folder_completeness_test = validation_processors.PackagePreservationComplete()
            preservation_folder_completeness_test.setup()
            preservation_folder_completeness_test.set_input(hathi_package.directories["preservation"])
            my_task.add_process(preservation_folder_completeness_test)

            # Access folder
            access_folder_completeness_test = validation_processors.PackageAccessComplete()
            access_folder_completeness_test.setup()
            access_folder_completeness_test.set_input(hathi_package.directories['access'])
            my_task.add_process(access_folder_completeness_test)

            # Preservation file name
            for file in os.scandir(hathi_package.directories["preservation"]):
                preservation_file_naming_test = validation_processors.PreservationFileNaming()
                preservation_file_naming_test.setup()
                preservation_file_naming_test.set_input(file.path)
                my_task.add_process(preservation_file_naming_test)

            # Access file name
            for file in os.scandir(hathi_package.directories["access"]):
                access_file_naming_test = validation_processors.AccessFileNaming()
                access_file_naming_test.setup()
                access_file_naming_test.set_input(file.path)
                my_task.add_process(access_file_naming_test)

            self.manager.push(my_task)

    def run(self):
        for i, task in enumerate(self.manager):
            print("({}/{}): {}".format(i + 1, len(self.manager), task.name))
            task.run()
            results = task.results
            if task.errors:
                print("errors = {}".format(len(task.errors)))
            if task.status == TaskStatus.SUCCESS:
                print("Package validation passed.")
            if task.status == TaskStatus.FAILED:
                print("Package validation Failed.")
                self.valid = False
            for result in results:
                if not result.valid:
                    print("      {}".format(result))
                    for error in result.errors:
                        self.errors.append(error)
                        print("      {}".format(error))


def get_package_folders(path) -> typing.Generator[packages.abs_package.AbsPackage, None, None]:
    warnings.warn("The run(path) function is deprecated. Use HathiQCRunner class instead", DeprecationWarning)
    with os.scandir(path) as search_path:
        for item in search_path:
            if item.is_dir():
                yield item.path


def get_packages(path):
    packages = []
    return packages


# Deprecated function
def run(path):
    warnings.warn("The run(path) function is deprecated. Use HathiQCRunner class instead", DeprecationWarning)
    hathi_packages_folders = get_package_folders(path)
    validation_success = True
    manager = task_manager.TaskManager()
    folder_errors = []

    # Setup tasks
    for folder in hathi_packages_folders:
        try:
            print("Searching for package in {}".format(folder))
            hathi_packages = packages.create_package("Hathi", folder)
            print("Found package in {}".format(folder))
            for hathi_package in hathi_packages:
                task_name = hathi_package.directories["preservation"].split(os.path.sep)[-1]

                my_task = tasks.Task(description="Validating {} in {}".format(task_name, hathi_package.root))
                # Package Completeness:
                package_completeness_test = validation_processors.PackageComplete()
                package_completeness_test.setup()
                package_completeness_test.set_input(hathi_package.root)
                my_task.add_process(package_completeness_test)

                # Preservation Folder
                preservation_folder_completeness_test = validation_processors.PackagePreservationComplete()
                preservation_folder_completeness_test.setup()
                preservation_folder_completeness_test.set_input(hathi_package.directories["preservation"])
                my_task.add_process(preservation_folder_completeness_test)

                # Access folder
                access_folder_completeness_test = validation_processors.PackageAccessComplete()
                access_folder_completeness_test.setup()
                access_folder_completeness_test.set_input(hathi_package.directories['access'])
                my_task.add_process(access_folder_completeness_test)

                # Preservation file name
                for file in os.scandir(hathi_package.directories["preservation"]):
                    preservation_file_naming_test = validation_processors.PreservationFileNaming()
                    preservation_file_naming_test.setup()
                    preservation_file_naming_test.set_input(file.path)
                    my_task.add_process(preservation_file_naming_test)

                # Access file name
                for file in os.scandir(hathi_package.directories["access"]):
                    access_file_naming_test = validation_processors.AccessFileNaming()
                    access_file_naming_test.setup()
                    access_file_naming_test.set_input(file.path)
                    my_task.add_process(access_file_naming_test)

                manager.push(my_task)
        except FileNotFoundError as e:
            error_message = "Unable to validate {}. Reason: {}".format(folder, e)
            print(error_message, file=sys.stderr)
            folder_errors.append(error_message)

    # run tasks
    for i, task in enumerate(manager):
        print("({}/{}): {}".format(i + 1, len(manager), task.name))
        task.run()
        results = task.results
        if task.errors:
            print("errors = {}".format(len(task.errors)))
        if task.status == TaskStatus.SUCCESS:
            print("Package validation passed.")
        if task.status == TaskStatus.FAILED:
            print("Package validation Failed.")
            validation_success = False
        for result in results:
            if not result.valid:
                print("      {}".format(result))
                for error in result.errors:
                    print("      {}".format(error))

    task_errors = functools.reduce(lambda lhs, rhs: lhs + rhs, [e.errors for e in manager], [])
    return validation_success, task_errors + folder_errors
