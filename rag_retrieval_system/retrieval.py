from typing import List
import config
from elasticsearch import Elasticsearch
import faiss
import numpy as np
from utils import llm_embed, logger

def retrieve_es_results(query: str, top_k: int) -> List[str]:
    es = Elasticsearch(f"http://{config.es_host}:{config.es_port}")
    index_name = "rag_index"
    
    # try:
    es_results = es.search(index=index_name, body={
        "query": {
            "match": {
                "index_text": query
            }
        },
        "size": top_k
    })
    es_node_ids = [hit["_source"]["node_ids"] for hit in es_results["hits"]["hits"]]
    logger.info(f"Retrieved {len(es_node_ids)} results from Elasticsearch for query: {query}")
    return es_node_ids
    # except Exception as e:
        # logger.error(f"Error retrieving results from Elasticsearch: {e}")
        # return []

def retrieve_faiss_results(query: str, top_k: int, struct_index) -> List[int]:
    # try:
    query_vector = np.array(llm_embed(query)).astype('float32').reshape(1, -1)
    faiss_index = faiss.read_index(config.faiss_index_path)
    _, faiss_indices = faiss_index.search(query_vector, top_k)
    logger.info(f"Retrieved {len(faiss_indices.flatten())} results from Faiss for query: {query}")
    indices = faiss_indices.flatten().tolist()
    keys = list(struct_index.table.keys())
    return [keys[index] for index in indices]
    # except Exception as e:
    #     logger.error(f"Error retrieving results from Faiss: {e}")
    #     return []
