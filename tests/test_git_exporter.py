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
        tree.create_node(tag="IM-TK", identifier=str(course_id), data=Course(
            subject="IM-TK",
            grade_level="tk",
            curricula_id=course_id,
            language="en",
            isbn=123456789,
            title="IM-TK"
        ))

        # Unit 1
        unit_id = uuid.uuid4()
        tree.create_node(tag="IM-TK-unit1", identifier=str(unit_id), parent=str(course_id), data=Unit(
            title="Unit 1",
            unit_number=unit_id
        ))

        # Unit 2
        unit_id = uuid.uuid4()
        tree.create_node(tag="IM-TK-unit2", identifier=str(unit_id), parent=str(course_id), data=Unit(
            title="Unit 2",
            unit_number=unit_id
        ))
        self.tree = tree

    def test_init(self):
        GitExporter("./repo", "test")

    def test_save_node(self):
        exporter = GitExporter("./repo", "test")
        course_node = self.tree.get_node(self.tree.root)
        exporter.save_node(course_node)

    def test_export(self):
        exporter = GitExporter("./repo")
        exporter.export(self.tree, message="national course")
        course_node = self.tree.get_node(self.tree.root)
        course_node.data.title = "IM-TK-Spanish"
        exporter.export(self.tree, message="spanish course")
