import abc
import contextlib
import os

class AbsHandler(contextlib.AbstractContextManager, metaclass=abc.ABCMeta):
    def open(self):
        pass

    def close(self):
        pass

    @abc.abstractmethod
    def write_data_line(self, payload):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __enter__(self):
        self.open()
        return self


class FileHandler(AbsHandler):
    def __init__(self, filename, overwrite=False):
        if os.path.exists(filename):
            if overwrite:
                os.remove(filename)
            else:
                raise FileExistsError(os.path.abspath(filename))
        self.filename = filename

    def write_data_line(self, payload):
        self.file.write("{}\n".format(payload))

    def close(self):
        self.file.close()

    def open(self):
        self.file = open(self.filename, "a")


class ConsoleHandler(AbsHandler):
    def write_data_line(self, payload):
        print(payload)
