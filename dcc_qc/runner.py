import logging

from dcc_qc import abs_runner, packages
from dcc_qc.profiles.profile import AbsProfile
from dcc_qc.validators import error_message
from dcc_qc.task_states import TaskStatus


class Runner(abs_runner.AbsRunner):
    packages = []

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

    def setup(self):

        package_searcher = self.profile.get_package_type
        package_searcher.root_path = self.path
        try:
            for package in package_searcher:
                self.packages.append(package)
        except packages.PackageError as e:
            self.valid = False
            new_error = error_message.ValidationError(e, group=self.path)
            new_error.source = self.path
            self.errors.append(new_error)

        for package in self.packages:
            self.manager.push(self.profile.create_validate_package_task(package))

    def __init__(self, entry_path, profile:AbsProfile):
        self.profile = profile

        super().__init__(entry_path)


