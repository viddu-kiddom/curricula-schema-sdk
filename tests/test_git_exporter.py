import copy
import uuid
from unittest import TestCase

from treelib import Tree

from curricula_schema_sdk.course import Course
from curricula_schema_sdk.exporters.git_exporter import GitExporter
from curricula_schema_sdk.unit import Unit


class TestGitExporter(TestCase):

    def build_tree(self) -> Tree:
        tree = Tree()

        # Course
        course_id = uuid.uuid4()
        tree.create_node(tag="IM-TK", identifier="IM-TK", data=Course(
            subject="IM-TK",
            grade_level="tk",
            curricula_id=course_id,
            language="en",
            isbn=123456789,
            title="IM-TK"
        ))

        # Unit 1
        unit_id = uuid.uuid4()
        tree.create_node(tag="IM-TK-unit1", identifier="IM-TK-unit1", parent="IM-TK", data=Unit(
            title="Unit 1",
            unit_number=unit_id
        ))

        # Unit 2
        unit_id = uuid.uuid4()
        tree.create_node(tag="IM-TK-unit2", identifier="IM-TK-unit2", parent="IM-TK", data=Unit(
            title="Unit 2",
            unit_number=unit_id
        ))
        return tree

    def test_export(self):
        exporter = GitExporter("./repo")

        national_tree = self.build_tree()
        # Save original tree as national tree
        national_oid = exporter.export(national_tree, commit_message="national course", branch_name="national")

        # Save spanish tree from national tree.
        spanish_tree = copy.deepcopy(national_tree)
        course_node = spanish_tree.get_node(spanish_tree.root)
        course_node.data.title = "IM-TK-Spanish"
        course_id = course_node.identifier

        # Unit 3
        unit_id = uuid.uuid4()
        spanish_tree.create_node(tag="IM-TK-unit3-spanish", identifier="IM-TK-unit3-spanish", parent=str(course_id),
                                 data=Unit(
                                     title="Unit 3",
                                     unit_number=unit_id
                                 ))
        exporter.export(spanish_tree, commit_message="spanish course", branch_name="spanish",
                        base_commit_oid=national_oid)

        # Modify national tree with a new commit
        modified_national_tree = copy.deepcopy(national_tree)
        course_node = modified_national_tree.get_node(modified_national_tree.root)
        course_node.data.title = "IM-TK-Modified"
        exporter.export(modified_national_tree, commit_message="modified course", branch_name="national",
                        base_commit_oid=national_oid)
