class ValidationError:
    source = ""

    def __init__(self, message, group=""):
        self.message = message
        self.group = group

    def __str__(self):
        if self.source:
            return "{}: {}".format(self.source, self.message)
        else:
            return self.message
