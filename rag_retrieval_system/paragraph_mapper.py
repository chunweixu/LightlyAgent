from typing import List
from data_structs import Node
from utils import logger

def map_and_deduplicate_results(retrieved: List[str], structure_index: dict) -> List[str]:
    unique_node_ids = []
    table = structure_index.table

    for node_id in retrieved:
        if node_id in table:
            unique_node_ids.extend(table[node_id])

    logger.info(f"Mapped and deduplicated {len(unique_node_ids)} node IDs from retrieved results")
    return unique_node_ids
