import logging
from pathlib import Path
from typing import Any

import pandas as pd
import pygit2
from pygit2 import Signature
from treelib import Tree

from curricula_schema_sdk.exporters.base_exporter import BaseExporter, EdgeType

logger = logging.getLogger(__name__)


class GitExporter(BaseExporter):

    def save_node(self, node) -> str:
        """
        Save the node to the repo as .json files
        :param node:
        :return:
        """
        data = node.data
        with open(f"{self.repo_path}/{node.identifier}.json", "w") as f:
            f.write(data.model_dump_json(indent=2))
        self.index.add(f"{node.identifier}.json")
        self.index.write()
        return str(node.identifier)

    def save_edge(self, node_id: str, edge_type: EdgeType = EdgeType.IS_CHILD_OF, parent_id: str = None):
        """
        Save the edge information to a csv file.
        :param parent_id:
        :param node_id:
        :param edge_type:
        :return:
        """
        # Load existing data
        try:
            df_existing = pd.read_csv(f"{self.repo_path}/edges.csv")
        except FileNotFoundError:
            df_existing = pd.DataFrame()

        df_new = pd.DataFrame([{
            "node_id": node_id,
            "edge_type": edge_type,
            "parent_id": parent_id
        }])
        df_merged = pd.concat([df_existing, df_new]).drop_duplicates(subset=["node_id"], keep="last")
        df_merged.to_csv(f"{self.repo_path}/edges.csv", index=False)
        self.index.add("edges.csv")
        self.index.write()

    def export(self, tree: Tree, **kwargs):
        # Collect kwargs
        commit_message = kwargs.get("commit_message", "Initial commit")
        branch_name = kwargs.get("branch_name", "main")
        base_commit_oid = kwargs.get("base_commit_oid")
        self.create_and_checkout_branch(base_commit_oid, branch_name)

        for node_id in tree.expand_tree():
            node = tree[node_id]
            save_id = self.save_node(node)
            self.save_edge(save_id, EdgeType.IS_CHILD_OF, node.predecessor(tree.identifier))

        tree = self.index.write_tree()

        # Everything is staged, now we can commit
        author = Signature(self.author_name, self.author_email)
        committer = author

        head = "HEAD" if self.repo.head_is_unborn else f"refs/heads/{branch_name}"
        parents = [] if base_commit_oid is None else [base_commit_oid]
        commit_oid = self.repo.create_commit(head, author, committer, commit_message, tree, parents)
        return commit_oid

    def create_and_checkout_branch(self, base_commit_oid: Any | None, branch_name: str):
        if base_commit_oid:
            base_commit = self.repo.get(base_commit_oid)
            # self.index.read_tree(base_commit.tree)
            # 2) Create a branch at that commit (fails if it exists already)
            try:
                self.repo.create_branch(branch_name, base_commit)
            except KeyError:
                logger.warning(f"Branch {branch_name} already exists. Skipping.")
                pass  # branch already exists
            # 3) Check out the new branch into the working tree
            self.repo.set_head(f"refs/heads/{branch_name}")
            self.repo.checkout_tree(base_commit, strategy=pygit2.GIT_CHECKOUT_FORCE)

    def __init__(self, repo_path: Path | str, author_name: str, author_email: str):

        if isinstance(repo_path, str):
            repo_path = Path(repo_path)
        self.repo_path = repo_path
        self.author_name = author_name
        self.author_email = author_email

        repo = pygit2.init_repository(repo_path, False)
        self.repo = repo

        index = repo.index
        self.index = index
