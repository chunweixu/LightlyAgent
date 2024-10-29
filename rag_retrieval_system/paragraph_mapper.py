from typing import List
from data_structs import Node
from utils import logger

def map_and_deduplicate_results(retrieved_ids: List[str], nodes: List[Node]) -> List[Node]:
    id_to_node = {str(node.id): node for node in nodes}
    unique_nodes = []
    seen_ids = set()

    for node_id in retrieved_ids:
        if node_id in id_to_node and node_id not in seen_ids:
            unique_nodes.append(id_to_node[node_id])
            seen_ids.add(node_id)

    logger.info(f"Mapped and deduplicated {len(unique_nodes)} nodes from retrieved results")
    return unique_nodes
