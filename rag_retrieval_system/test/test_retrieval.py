from indexer import ESIndexer
from retriever import ESRetriever
from data_structs import Node

def test_search_system():
    # 1. 准备测试数据
    test_nodes = [
        Node(
            text="Elasticsearch is a powerful search engine based on Lucene",
            metadata={"source": "test"}
        ),
        Node(
            text="Vector search enables semantic similarity matching",
            metadata={"source": "test"}
        ),
        Node(
            text="Text search uses inverted indices for fast retrieval",
            metadata={"source": "test"}
        )
    ]

    # 2. 构建索引
    indexer = ESIndexer()
    
    # 创建索引
    indexer.create_literal_index()
    indexer.create_vector_index()
    
    # 索引文档
    indexer.index_literal_documents(test_nodes)
    indexer.index_vector_documents(test_nodes)

    # 3. 测试检索
    retriever = ESRetriever()
    
    # 测试文本检索
    print("\nLiteral Search Results:")
    results = retriever.literal_search("search engine")
    for hit in results:
        print(f"Score: {hit['_score']}, Text: {hit['_source']['text']}")

    # 测试向量检索
    print("\nVector Search Results:")
    results = retriever.vector_search("semantic search")
    for hit in results:
        print(f"Score: {hit['_score']}, Text: {hit['_source']['text']}")

    # 测试混合检索
    print("\nHybrid Search Results:")
    results = retriever.hybrid_search("search technology")
    for result in results:
        print(f"Total Score: {result['literal_score'] + result['vector_score']}, "
              f"Text: {result['text']}")

if __name__ == "__main__":
    test_search_system() 