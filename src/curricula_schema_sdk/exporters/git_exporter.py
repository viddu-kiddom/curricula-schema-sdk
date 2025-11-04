from wsgiref.validate import header_re

import pygit2
from pygit2 import Signature
from treelib import Tree

from curricula_schema_sdk.exporters.base_exporter import BaseExporter


class GitExporter(BaseExporter):

    def save_node(self, node) -> str:
        data = node.data
        with open(f"{self.repo_path}/{node.identifier}.json", "w") as f:
            f.write(data.model_dump_json(indent=2))
        self.repo.index.add(f"{node.identifier}.json")
        self.repo.index.write()
        return str(node.identifier)

    def save_edge(self, parent_id, child_id, edge_type):
        with open(f"{self.repo_path}/edges.csv", "a") as f:
            f.write(f"{parent_id},{child_id},{edge_type},{self.branch_name}\n")
        self.repo.index.add("edges.csv")
        self.repo.index.write()

    def export(self, tree: Tree, **kwargs):
        for node_id in tree.expand_tree():
            node = tree[node_id]
            rev_id = self.save_node(node)
            self.save_edge(node.predecessor(tree.identifier), rev_id, "isParentOf")

        author = Signature(kwargs.get("author_name", "Viddu Devigere"), kwargs.get("author_email", "viddu@kiddom.co"))
        committer = author
        message = kwargs.get("commit_message", "Initial commit")
        tree = self.repo.index.write_tree()
        commit_oid = self.repo.create_commit(self.head_ref, author, committer, message, tree, self.parents)
        commit = self.repo.get(commit_oid)
        if self.branch_name != "main":
            self.repo.create_branch(self.branch_name, commit)
        self.head_ref = self.repo.head.name
        self.parents = [self.repo.head.target]

    def loadTree(self) -> Tree:
        pass

    def __init__(self, repo_path, branch_name="main"):
        self.repo_path = repo_path
        self.branch_name = branch_name
        self.repo = pygit2.init_repository(repo_path, False)
        self.head_ref = "HEAD" if self.repo.head_is_unborn else self.repo.head.name
        self.parents = [] if self.repo.head_is_unborn else [self.repo.head.target]
