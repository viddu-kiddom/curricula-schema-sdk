from treelib import Tree

from curricula_schema_sdk.exporters.base_exporter import BaseExporter


class PostgresEAVExporter(BaseExporter):
    def export(self, tree: Tree):
        raise Exception("Not implemented yet")

    def __init__(self, connection_string):
        self.connection_string = connection_string
