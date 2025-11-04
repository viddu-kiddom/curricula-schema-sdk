import uuid
from unittest import TestCase

from treelib import Tree

from curricula_schema_sdk.course import Course
from curricula_schema_sdk.exporters.git_exporter import GitExporter
from curricula_schema_sdk.unit import Unit


class TestGitExporter(TestCase):

    def setUp(self):
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
        self.tree = tree

    def test_init(self):
        GitExporter("./repo")

    def test_save_node(self):
        exporter = GitExporter("./repo")
        course_node = self.tree.get_node(self.tree.root)
        exporter.save_node(course_node)

    def test_export(self):
        # Save original tree as national tree
        exporter = GitExporter("./repo")
        exporter.export(self.tree, commit_message="national course", branch_name="national")

        # Modify national tree with a new commit

        # Save spanish tree from national tree.
        spanish_tree = self.tree
        course_node = spanish_tree.get_node(spanish_tree.root)
        course_node.data.title = "IM-TK-Spanish"
        course_id = course_node.identifier

        # Unit 3
        unit_id = uuid.uuid4()
        spanish_tree.create_node(tag="IM-TK-unit3-spanish", identifier="IM-TK-unit3-spanish", parent=str(course_id), data=Unit(
            title="Unit 3",
            unit_number=unit_id
        ))
        exporter.export(spanish_tree, commit_message="spanish course", branch_name="spanish")
