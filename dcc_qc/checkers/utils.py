from .check_suite import CheckSuiteFactory, AbsCheckSuite


def get_check_suite(name)-> AbsCheckSuite:
    factory = CheckSuiteFactory()
    new_validator = factory.create_instance(name)
    return new_validator
