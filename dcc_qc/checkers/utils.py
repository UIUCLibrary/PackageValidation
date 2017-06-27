from .validator_factory import ValidatorFactory

def get_validator(name):
    factory = ValidatorFactory()
    new_validator = factory.create_instance(name)
    return new_validator