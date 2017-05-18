class Results:
    def __init__(self, result_type, valid, errors):
        self._name = result_type
        self._valid = valid
        self._errors = errors

    @property
    def result_type(self):
        return self._name

    @property
    def valid(self) -> bool:
        return self._valid

    @property
    def errors(self) -> list:
        return self._errors

    def __str__(self) -> str:
        return "The result of {} {} valid.".format(self._name, "is not" if not self.valid else "is")


