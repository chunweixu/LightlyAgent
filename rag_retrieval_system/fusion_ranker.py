from typing import List
from utils import logger

def fusion_ranker(es_results: List[str], faiss_results: List[int], top_k: int = 5) -> List[str]:
    if not es_results: return faiss_results[:top_k]
    if not faiss_results: return es_results[:top_k]
    rank_scores = {}
    # Assign scores based on rank positions from Elasticsearch and Faiss results
    for i, node_id in enumerate(es_results):
        rank_scores[node_id] = rank_scores.get(node_id, 0) + 1 / (i + 1)
    for i, node_id in enumerate(faiss_results):
        rank_scores[str(node_id)] = rank_scores.get(str(node_id), 0) + 1 / (i + 1)
    
    # Sort by score in descending order and return the top-k node IDs, ensuring uniqueness
    sorted_nodes = sorted(rank_scores.keys(), key=lambda x: rank_scores[x], reverse=True)
    top_results = sorted_nodes[:top_k]
    logger.info(f"Fusion ranker produced top {top_k} results: {top_results}")
    return top_results
