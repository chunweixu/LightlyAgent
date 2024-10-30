
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import numpy as np

# Initialize Elasticsearch
es = Elasticsearch("http://localhost:9200", verify_certs=False)

# Ensure the Elasticsearch instance is available
if not es.ping():
    raise ValueError("Connection failed. Please make sure Elasticsearch is running and accessible.")

# 1. Text-based Literal Recall - Indexing and Searching

def create_literal_index():
    index_name = "literal_index"
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    
    # Define the literal index mapping
    mapping = {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"}
            }
        }
    }
    es.indices.create(index=index_name, body=mapping)
    if es.indices.exists(index="literal_index"):
        print("Literal index created successfully")
    else:
        print("Failed to create literal index")



def index_literal_data():
    # Sample data for indexing
    documents = [
        {"_index": "literal_index", "_id": 1, "title": "Elasticsearch Tutorial", "content": "Learn how to use Elasticsearch for text search."},
        {"_index": "literal_index", "_id": 2, "title": "Elasticsearch and Python", "content": "Integration of Elasticsearch with Python using elasticsearch-py."},
        {"_index": "literal_index", "_id": 3, "title": "Advanced Elasticsearch", "content": "Understanding full-text search and filtering in Elasticsearch."},
    ]
    # bulk(es, documents)
    success, _ = bulk(es, documents)
    if success:
        print(f"Successfully indexed {len(documents)} documents")
    else:
        print("Failed to index documents")


def search_literal(query):
    # Search for a keyword in literal index
    response = es.search(
        index="literal_index",
        body={
            "query": {
                "match": {
                    "content": query
                }
            }
        }
    )
    print("Literal Search Results:")
    for hit in response['hits']['hits']:
        print(f"ID: {hit['_id']}, Score: {hit['_score']}, Content: {hit['_source']['content']}")

# response = es.search(index="literal_index", body={"query": {"match_all": {}}})
# print("All Documents in Index:")
# for hit in response['hits']['hits']:
#     print(f"ID: {hit['_id']}, Content: {hit['_source']}")

# 2. Vector-based Semantic Recall - Indexing and Searching

def create_vector_index():
    index_name = "vector_index"
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    
    # Define the vector index mapping
    mapping = {
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content_vector": {
                    "type": "dense_vector",
                    "dims": 3  # Example with vector dimension of 3
                }
            }
        }
    }
    es.indices.create(index=index_name, body=mapping)
    if es.indices.exists(index="vector_index"):
        print("Literal index created successfully")
    else:
        print("Failed to create literal index")



def index_vector_data():
    # Sample vectors (generated arbitrarily for demonstration purposes)
    documents = [
        {"_index": "vector_index", "_id": 1, "title": "Elasticsearch Tutorial", "content_vector": [0.1, 0.3, 0.9]},
        {"_index": "vector_index", "_id": 2, "title": "Elasticsearch and Python", "content_vector": [0.2, 0.8, 0.3]},
        {"_index": "vector_index", "_id": 3, "title": "Advanced Elasticsearch", "content_vector": [0.4, 0.4, 0.7]},
    ]
    # bulk(es, documents)
    success, _ = bulk(es, documents)
    if success:
        print(f"Successfully indexed {len(documents)} documents")
    else:
        print("Failed to index documents")


def search_vector(query_vector):
    # Semantic search using a query vector
    response = es.search(
        index="vector_index",
        body={
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'content_vector') + 1.0",
                        "params": {"query_vector": query_vector}
                    }
                }
            }
        }
    )
    print("Vector Search Results:")
    for hit in response['hits']['hits']:
        print(f"ID: {hit['_id']}, Score: {hit['_score']}, Title: {hit['_source']['title']}")

response = es.search(index="vector_index", body={"query": {"match_all": {}}})
print("All Documents in Index:")
for hit in response['hits']['hits']:
    print(f"ID: {hit['_id']}, Content: {hit['_source']}")


if __name__ == "__main__":
    # Literal recall - indexing and searching
    create_literal_index()
    index_literal_data()
    search_literal("Elasticsearch")

    # Vector recall - indexing and searching
    create_vector_index()
    index_vector_data()
    search_vector([0.2, 0.7, 0.5])
