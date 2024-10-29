from typing import List
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import TokenTextSplitter
import os

def parse_documents(document_path: str, chunk_size: int, overlap: int):
    if not os.path.exists(document_path):
        raise FileNotFoundError(f"Document path {document_path} does not exist.")

    documents = SimpleDirectoryReader(document_path).load_data()
    text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = []

    for doc in documents:
        chunks.extend(text_splitter.split_text(doc.text))

    return chunks
