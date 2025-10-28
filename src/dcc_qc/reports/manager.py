import abc
from .handler import AbsHandler


class ReportManager(metaclass=abc.ABCMeta):
    _handlers = set()  # type: ignore

    def add_handler(self, handler: AbsHandler):
        self._handlers.add(handler)

    def detach_handler(self, handler: AbsHandler):
        self._handlers.remove(handler)

    def write_line(self, text=""):
        for handle in self._handlers:
            with handle as writer:
                writer.write_data_line(text)
            # handle.open()
            # handle.write_data_line(text)
            # handle.close()
