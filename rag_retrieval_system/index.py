from typing import List
from data_structs import Node, StructIndex
from utils import llm, llm_embed, logger, get_prompt
from config import Config
from elasticsearch import Elasticsearch
import faiss
import numpy as np

def generate_index(nodes: List[Node], index_types: List[str] = ["Original"]) -> List[Node]:
    for node in nodes:
        if "Original" in index_types:
            node.index.add(node.text)
            logger.info(f"Original index generated for node {node.id}")
        if "Summary" in index_types:
            summary_prompt = get_prompt("summary")
            summary = llm(summary_prompt.format(text=node.text))
            node.index.add(summary)
            logger.info(f"Summary index generated for node {node.id}")
        if "Enhance" in index_types:
            enhance_prompt = get_prompt("enhance")
            enhancement = llm(enhance_prompt.format(text=node.text))
            enhancement_items = [item.strip() for item in enhancement.split('###') if item.strip()]
            for item in enhancement_items[:5]:  # Limit to 3-5 items
                node.index.add(item)
            logger.info(f"Enhance index generated for node {node.id}")
    return nodes

def map_index_to_paragraphs(nodes: List[Node]) -> StructIndex:
    struct_index = StructIndex()
    for node in nodes:
        for idx in node.index:
            if idx not in struct_index.table:
                struct_index.table[idx] = set()
            struct_index.table[idx].add(str(node.id))
    logger.info(f"StructIndex created with {len(struct_index.table)} entries")
    return struct_index

def build_es_index(struct_index: StructIndex):
    config = Config()
    es = Elasticsearch([{'host': config.es_host, 'port': config.es_port}])
    index_name = "rag_index"
    try:
        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name)
            logger.info(f"Created Elasticsearch index: {index_name}")
        for idx, node_ids in struct_index.table.items():
            es.index(index=index_name, body={
                'index_text': idx,
                'node_ids': list(node_ids)
            })
            logger.info(f"Indexed text: {idx} with node_ids: {list(node_ids)}")
    except Exception as e:
        logger.error(f"Error building Elasticsearch index: {e}")

def build_faiss_index(struct_index: StructIndex):
    config = Config()
    try:
        vectors = [llm_embed(idx) for idx in struct_index.table.keys()]
        vectors = np.array(vectors).astype('float32')
        dimension = vectors.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(vectors)
        faiss.write_index(index, config.faiss_index_path)
        logger.info(f"Faiss index built and saved at {config.faiss_index_path}")
    except Exception as e:
        logger.error(f"Error building Faiss index: {e}")
