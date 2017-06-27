from . import check_suite


def get_check_suite(name)->check_suite.AbsCheckSuite:
    factory = check_suite.CheckSuiteFactory()
    new_validator = factory.create_instance(name)
    return new_validator
