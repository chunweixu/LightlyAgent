from data_parser import parse_documents
from index import generate_index, map_index_to_paragraphs, build_es_index, build_faiss_index
from retrieval import retrieve_es_results, retrieve_faiss_results
from fusion_ranker import fusion_ranker
from paragraph_mapper import map_and_deduplicate_results
from config import Config
from utils import logger
from typing import List


config = Config()

def main():
    try:
        logger.info("Step 1: Parsing documents...")
        document_path = "/Users/smiling/Project/LightlyAgent/data/test"
        nodes = parse_documents(document_path, config.chunk_size, config.overlap)
        logger.info(f"Parsed {len(nodes)} nodes from documents.")

        logger.info("Step 2: Generating indexes for nodes...")
        nodes = generate_index(nodes, index_types=list(config.index_types))
        struct_index = map_index_to_paragraphs(nodes)

        logger.info("Step 3: Building Elasticsearch and Faiss indices...")
        build_es_index(struct_index)
        build_faiss_index(struct_index)

        logger.info("Step 4: Retrieving results for a sample query...")
        query = "sample query"
        top_k = 5
        es_results = retrieve_es_results(query, top_k=top_k)
        faiss_results = retrieve_faiss_results(query, top_k=top_k)

        logger.info("Step 5: Applying fusion ranker...")
        top_results = fusion_ranker(es_results, faiss_results, top_k=top_k)
        logger.info(f"Fusion ranker produced top {top_k} results: {top_results}")

        logger.info("Step 6: Mapping and deduplicating results...")
        unique_nodes = map_and_deduplicate_results(top_results, nodes)
        logger.info(f"Mapped and deduplicated to {len(unique_nodes)} unique nodes.")

        print(f"Final top results:")
        for node in unique_nodes:
            print(f"Node ID: {node.id}, Text: {node.text[:50]}...")
    except Exception as e:
        logger.error(f"Error occurred in main workflow: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
