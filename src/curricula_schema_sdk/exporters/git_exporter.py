import pygit2
from pygit2 import Signature
from treelib import Tree

from curricula_schema_sdk.exporters.base_exporter import BaseExporter


class GitExporter(BaseExporter):

    def save_node(self, node, **kwargs) -> str:
        """
        Save the node to the repo as .json files
        :param node:
        :return:
        """
        data = node.data
        with open(f"{self.repo_path}/{node.identifier}.json", "w") as f:
            f.write(data.model_dump_json(indent=2))
        self.repo.index.add(f"{node.identifier}.json")
        self.repo.index.write()
        return str(node.identifier)

    def save_edge(self, parent_id, child_id, edge_type, **kwargs):
        """
        Save the edge information along with the branch details to a csv file.
        :param parent_id:
        :param child_id:
        :param edge_type:
        :return:
        """
        with open(f"{self.repo_path}/edges.csv", "a") as f:
            f.write(f"{parent_id},{child_id},{edge_type},{kwargs.get("branch_name")}\n")
        self.repo.index.add("edges.csv")
        self.repo.index.write()

    def export(self, tree: Tree, **kwargs):
        for node_id in tree.expand_tree():
            node = tree[node_id]
            node_id = self.save_node(node)
            self.save_edge(node.predecessor(tree.identifier), node_id, "isParentOf", **kwargs)

        author = Signature(kwargs.get("author_name", "Viddu Devigere"), kwargs.get("author_email", "viddu@kiddom.co"))
        committer = author
        message = kwargs.get("commit_message", "Initial commit")
        tree = self.repo.index.write_tree()
        head = "HEAD" if self.repo.head_is_unborn else self.repo.head.name
        parents = [] if self.repo.head_is_unborn else [self.repo.head.target]
        commit_oid = self.repo.create_commit(head, author, committer, message, tree, parents)
        branch_name = kwargs.get("branch_name", "main")
        if branch_name != "main":
            self.repo.create_branch(branch_name, self.repo.get(commit_oid))

    def loadTree(self) -> Tree:
        pass

    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.repo = pygit2.init_repository(repo_path, False)
