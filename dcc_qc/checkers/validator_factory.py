from inspect import getmembers, isclass, isabstract
from dcc_qc.checkers.abs_checkers import AbsChecker
from dcc_qc import checkers


class CheckersFactory:
    validators = {}

    def __init__(self):
        self.load_validators()

    def load_validators(self):

        classes = getmembers(checkers, lambda m: isclass(m) and not isabstract(m))
        for name, _type in classes:
            if isclass(_type) and issubclass(_type, AbsChecker):
                self.validators.update([[name, _type]])

    def create_instance(self, name):
        return self.validators[name]()
