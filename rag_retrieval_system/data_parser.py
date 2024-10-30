from typing import List
from data_structs import Node
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

    nodes = chunks_to_nodes(chunks)

    return nodes

def chunks_to_nodes(chunks: List[str]):
    nodes = []
    for chunk in chunks:
        node = Node()  # 假设Node是一个已定义的类
        node.text = chunk
        nodes.append(node)
    return nodes


