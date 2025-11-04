from abc import ABC, abstractmethod

from treelib import Tree


class BaseExporter(ABC):

    @abstractmethod
    def save_node(self, node) -> str:
        pass

    @abstractmethod
    def save_edge(self, parent_id, child_id, edge_type):
        pass

    def export(self, tree: Tree, **kwargs):
        for node_id in tree.expand_tree():
            node = tree[node_id]
            rev_id = self.save_node(node)
            self.save_edge(node.predecessor(tree.identifier), rev_id, "isParentOf")
