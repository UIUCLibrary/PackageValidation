from inspect import getmembers, isclass, isabstract
import inspect
from dcc_qc import profiles
from . import profile

class ProfileFactory:
    profiles = {}  # type: ignore

    def __init__(self):
        self.load_packages()

    def load_packages(self):
        classes = getmembers(profiles, lambda m: isclass(m) and not isabstract(m))
        for name, _type in classes:
            if isclass(_type) and issubclass(_type, profile.AbsProfile):
                self.profiles.update([[_type.profile_name.lower(), _type]])

    def create_instance(self, profile_name):
        return self.profiles[profile_name]()
