import abc
import typing
from collections import namedtuple

PackageItem = namedtuple("PackageItem", ["root", "directories"])

class AbsPackage(metaclass=abc.ABCMeta):
    def __init__(self, root_path):
        self.root_path = root_path
        self._items = []
        self.load()

    @property
    @abc.abstractmethod
    def items(self)->typing.Generator[PackageItem, None, None]:
        pass

    @abc.abstractmethod
    def load(self):
        pass

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        for i in self.items:
            yield i
