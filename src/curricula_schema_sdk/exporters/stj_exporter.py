from treelib import Tree

from curricula_schema_sdk.exporters.base_exporter import BaseExporter


class SimpleTreeJsonExporter(BaseExporter):
    def export(self, tree: Tree):
        raise Exception("Not implemented yet")
