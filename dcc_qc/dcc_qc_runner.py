"""
This will become a script but for now it's just a sample implementation. 
I'm using it to check that my validators work and my package API make 
sense when it is consumed by a script.
"""
import os
import typing

from dcc_qc import task_manager, tasks, packages
from dcc_qc import validation_processors

TEST_PATH = "T:/HenryTest-PSR_2/DCC\Package_GOOD/"


def get_package_folders(path)->typing.Generator[packages.abs_package.AbsPackage, None, None]:
    with os.scandir(path) as search_path:
        for item in search_path:
            if item.is_dir():
                yield item.path


def get_packages(path):
    packages = []
    return packages


def main():
    # packages = get_packages(TEST_PATH)
    hathi_packages_folders = get_package_folders(TEST_PATH)

    manager = task_manager.TaskManager()

    # Setup tasks
    for folder in hathi_packages_folders:
        hathi_packages = packages.create_package("Hathi", folder)
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


            manager.push(my_task)

    # run tasks
    for i, task in enumerate(manager):
        print("({}/{}): {}".format(i + 1, len(manager), task.name))
        task.run()
        results = task.results
        if task.errors:
            print("errors = {}".format(len(task.errors)))

        for result in results:
            if not result.valid:
                print("      {}".format(result))
                for error in result.errors:
                    print("      {}".format(error))


if __name__ == '__main__':
    main()
