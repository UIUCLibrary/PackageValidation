"""
This will become a script but for now it's just a sample implementation. 
I'm using it to check that my validators work and my package API make 
sense when it is consumed by a script.
"""

import os
import typing
import functools
import logging
import warnings
import sys

from dcc_qc import task_manager, tasks, packages
from dcc_qc import validation_processors
from dcc_qc.abs_runner import AbsRunner
from dcc_qc.task_states import TaskStatus
from dcc_qc.validators import error_message
warnings.warn("{} is deprecated. Use runner.py".format(__name__), DeprecationWarning)

class HathiQCRunner(AbsRunner):
    @staticmethod
    def get_package_folders(path) -> typing.Generator[str, None, None]:
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
            new_error = error_message.ValidationError(e, group=self.path)
            new_error.source = self.path
            self.errors.append(new_error)

        # Add the tasks that need to be validated
        for hathi_package in self.packages:
            task_name = hathi_package.directories["preservation"].split(os.path.sep)[-1]

            my_task = tasks.Task(description="Validating {} in {}".format(task_name, hathi_package.root))

            # Package Structure Completeness:
            package_structure_test = validation_processors.PackageStructureComplete()
            package_structure_test.setup()
            package_structure_test.set_input(hathi_package.root)
            my_task.add_process(package_structure_test)

            # Package component Completeness:
            package_component_test = validation_processors.PackageComponentComplete()
            package_component_test.setup()
            package_component_test.set_input(hathi_package)
            my_task.add_process(package_component_test)

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
        logger = logging.getLogger(__name__)
        for i, task in enumerate(self.manager):
            logger.info("({}/{}) Starting: {}".format(i + 1, len(self.manager), task.name))
            task.run()
            results = task.results
            if task.errors:
                logger.info("{} had {} errors.".format(task.name, len(task.errors)))
            if task.status == TaskStatus.SUCCESS:
                logger.info("Task : {} passed.".format(task.name))
            if task.status == TaskStatus.FAILED:
                logger.info("Task : {} failed.".format(task.name))
                self.valid = False
            for result in results:
                if not result.valid:
                    # print("      {}".format(result))
                    for validation_error in result.errors:
                        assert isinstance(validation_error, error_message.ValidationError)
                        self.errors.append(validation_error)
                        logger.info("Validation failure: {}: {}".format(task.name, validation_error))


def get_package_folders(path) -> typing.Generator[packages.abs_package.AbsPackage, None, None]:
    warnings.warn("The run(path) function is deprecated. Use HathiQCRunner class instead", DeprecationWarning)
    with os.scandir(path) as search_path:
        for item in search_path:
            if item.is_dir():
                yield item.path


def get_packages(path):
    packages = []
    return packages
