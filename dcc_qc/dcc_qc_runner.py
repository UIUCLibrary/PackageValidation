"""
This will become a script but for now it's just a sample implementation. 
I'm using it to check that my validators work and my package API make 
sense when it is consumed by a script.
"""
import os

import tasks
from dcc_qc import task_manager
from dcc_qc import validation_processors

TEST_PATH = "Z:/MedusaStaging/MappingHistory_Archives/20170323_MappingHistory"
# TEST_PATH = "T:\HenryTest-PSR_2\DCC\Preservation_BAD"


# TEST_PATH = "T:\HenryTest-PSR_2\DCC\Preservation_GOOD"


def get_package_folders(path):
    with os.scandir(path) as search_path:
        for item in search_path:
            if item.is_dir():
                yield item.path


def main():
    packages = get_package_folders(TEST_PATH)
    manager = task_manager.TaskManager()

    # Setup tasks
    for path in packages:
        my_task = tasks.Task(name=path)

        preservation_package_test = validation_processors.PackagePreservationComplete()
        preservation_package_test.setup()
        preservation_package_test.set_input(path)
        my_task.add_process(preservation_package_test)

        manager.push(my_task)

    # run tasks
    for i, task in enumerate(manager):
        print("({}/{}) Checking: {}".format(i + 1, len(manager), task.name))
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
