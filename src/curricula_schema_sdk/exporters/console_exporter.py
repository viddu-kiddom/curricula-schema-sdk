import uuid

from curricula_schema_sdk.exporters.base_exporter import BaseExporter


class ConsoleExporter(BaseExporter):
    def save_node(self, node) -> str:
        print(f"Saving {node.data.model_dump_json(indent=2)}")
        return str(node.identifier)

    def save_edge(self, parent_id, child_id, edge_type):
        print(f"Saving edge {parent_id} - ({edge_type}) -> {child_id}")
