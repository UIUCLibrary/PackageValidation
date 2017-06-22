from .profile_factory import ProfileFactory
from .profile import AbsProfile

def get_available():
    factory = ProfileFactory()
    return factory.profiles.keys()

def get_profile(factory_name) -> AbsProfile:
    factory = ProfileFactory()
    new_profile = factory.create_instance(factory_name.lower())
    return new_profile