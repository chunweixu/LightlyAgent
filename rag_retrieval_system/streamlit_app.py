import streamlit as st
from typing import List
from data_structs import Node
from index import generate_index, map_index_to_paragraphs, build_es_index, build_faiss_index
from retrieval import retrieve_es_results, retrieve_faiss_results
from fusion_ranker import fusion_ranker
from paragraph_mapper import map_and_deduplicate_results
from config import Config
from data_parser import parse_documents
from utils import logger

config = Config()

def main():
    st.title("RAG System with Streamlit")

    # Input parameters
    st.sidebar.header("Knowledge Base Generation Parameters")
    chunk_size = st.sidebar.number_input("Chunk Size", min_value=1, value=config.chunk_size, step=1)
    overlap = st.sidebar.number_input("Overlap Size", min_value=0, value=config.overlap, step=1)
    index_types = st.sidebar.multiselect("Index Types", ["Original", "Summary", "Enhance"], list(config.index_types))
    document_path = st.sidebar.text_input("Document Path", "./documents")
    top_k = st.sidebar.number_input("Top-K Results", min_value=1, value=5, step=1)

    # Knowledge Base Generation Section
    st.header("Knowledge Base Generation")
    if st.button("Generate Knowledge Base"):
        if not document_path:
            st.error(f"Document path cannot be empty.")
        else:
            st.info("Loading documents and creating nodes...")
            try:
                nodes = parse_documents(document_path, chunk_size, overlap)
                st.success(f"Parsed {len(nodes)} nodes from documents.")

                st.info("Generating indexes for nodes...")
                nodes = generate_index(nodes, index_types=index_types)
                struct_index = map_index_to_paragraphs(nodes)

                st.info("Building Elasticsearch and Faiss indices...")
                build_es_index(struct_index)
                build_faiss_index(struct_index)
                st.success("Knowledge Base generated successfully!")
            except Exception as e:
                logger.error(f"Error generating knowledge base: {e}")
                st.error(f"Error generating knowledge base: {e}")

    # Retrieval Section
    st.header("Query Retrieval")
    query = st.text_input("Enter your query:")
    if st.button("Retrieve Results"):
        if query:
            st.info("Retrieving results...")
            try:
                es_results = retrieve_es_results(query, top_k=top_k)
                faiss_results = retrieve_faiss_results(query, top_k=top_k)
                top_results = fusion_ranker(es_results, faiss_results, top_k=top_k)

                unique_nodes = map_and_deduplicate_results(top_results, nodes)

                st.success(f"Top {top_k} Results:")
                for node in unique_nodes:
                    st.write(f"Node ID: {node.id}, Text: {node.text[:200]}...")
            except Exception as e:
                logger.error(f"Error retrieving results: {e}")
                st.error(f"Error retrieving results: {e}")
        else:
            st.error("Please enter a query to retrieve results.")

if __name__ == "__main__":
    main()
