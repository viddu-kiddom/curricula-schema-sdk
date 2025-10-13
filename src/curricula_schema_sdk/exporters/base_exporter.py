from abc import ABC, abstractmethod

from treelib import Tree


class BaseExporter(ABC):
    @abstractmethod
    def export(self, tree: Tree):
        pass