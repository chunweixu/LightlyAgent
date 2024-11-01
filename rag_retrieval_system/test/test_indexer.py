from indexer import ESIndexer
from data_structs import Node

# 创建测试数据
test_nodes = [
    Node(
        text="This is a test document about Elasticsearch",
        metadata={"source": "test"}
    ),
    Node(
        text="Another test document about vector search",
        metadata={"source": "test"}
    )
]

# 初始化索引器
indexer = ESIndexer()

# 创建索引
indexer.create_literal_index()
indexer.create_vector_index()

# 索引文档
indexer.index_literal_documents(test_nodes)
indexer.index_vector_documents(test_nodes) 