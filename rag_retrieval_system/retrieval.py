from typing import List
from config import Config
from elasticsearch import Elasticsearch
import faiss
import numpy as np
from utils import llm_embed, logger

def retrieve_es_results(query: str, top_k: int) -> List[str]:
    config = Config()
    es = Elasticsearch([{'host': config.es_host, 'port': config.es_port}])
    index_name = "rag_index"
    
    try:
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
    except Exception as e:
        logger.error(f"Error retrieving results from Elasticsearch: {e}")
        return []

def retrieve_faiss_results(query: str, top_k: int) -> List[int]:
    config = Config()
    try:
        query_vector = np.array(llm_embed(query)).astype('float32').reshape(1, -1)
        faiss_index = faiss.read_index(config.faiss_index_path)
        _, faiss_indices = faiss_index.search(query_vector, top_k)
        logger.info(f"Retrieved {len(faiss_indices.flatten())} results from Faiss for query: {query}")
        return faiss_indices.flatten().tolist()
    except Exception as e:
        logger.error(f"Error retrieving results from Faiss: {e}")
        return []
