"""
This will become a script but for now it's just a sample implementation. 
I'm using it to check that my validators work and my package API make 
sense when it is consumed by a script.
"""
import os
import typing
import functools

import sys

from dcc_qc import task_manager, tasks, packages
from dcc_qc import validation_processors


# TODO: Refactor me!
from dcc_qc.task_states import TaskStatus


def get_package_folders(path) -> typing.Generator[packages.abs_package.AbsPackage, None, None]:
    with os.scandir(path) as search_path:
        for item in search_path:
            if item.is_dir():
                yield item.path


def get_packages(path):
    packages = []
    return packages


# TODO: refactor into own class
def run(path):
    hathi_packages_folders = get_package_folders(path)

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
        for result in results:
            if not result.valid:
                print("      {}".format(result))
                for error in result.errors:
                    print("      {}".format(error))

    task_errors = functools.reduce(lambda lhs, rhs: lhs + rhs, [e.errors for e in manager], [])
    return task_errors + folder_errors
