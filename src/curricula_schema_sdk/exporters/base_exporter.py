from abc import ABC, abstractmethod
from enum import StrEnum

from treelib import Tree


class EdgeType(StrEnum):
    IS_CHILD_OF = "isChildOf"


class BaseExporter(ABC):

    @abstractmethod
    def save_node(self, node) -> str:
        pass

    @abstractmethod
    def save_edge(self, node_id: str, edge_type: EdgeType = EdgeType.IS_CHILD_OF, parent_id: str = None):
        pass

    def export(self, tree: Tree, **kwargs):
        for node_id in tree.expand_tree():
            node = tree[node_id]
            save_id = self.save_node(node)
            self.save_edge(save_id, EdgeType.IS_CHILD_OF, node.predecessor(tree.identifier))
