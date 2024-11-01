import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(sys.path)

from data_parser import parse_documents
from storage import Storage
from indexer import ESIndexer
from retriever import ESRetriever
import config
from utils import logger

def setup_test_data():
    """准备测试数据"""
    test_dir = os.path.join(os.path.dirname(__file__), "test_data")
    os.makedirs(test_dir, exist_ok=True)
    test_file = os.path.join(test_dir, "test.txt")
    
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("""This is a test document about Elasticsearch and vector search.
        It contains multiple paragraphs for testing.
        
        This is another paragraph about information retrieval and search systems.
        We can use this to test our document processing pipeline.
        
        The final paragraph discusses vector embeddings and semantic search capabilities.""")
    
    return test_dir

def test_document_processing():
    """测试文档处理流程"""
    # try:
    print("\n=== 开始测试文档处理流程 ===")
    
    # 1. 准备测试数据
    print("\n1. 准备测试数据...")
    test_dir = "/Users/smiling/Project/LightlyAgent/data/test"
    
    # 2. 测试文档解析
    print("\n2. 测试文档解析...")
    nodes = parse_documents(test_dir, config.chunk_size, config.overlap)
    print(f"解析得到 {len(nodes)} 个节点")
    for node in nodes:
        print(f"- Node {node.id[:8]}: {node.text[:50]}...")
    
    # 3. 测试数据存储
    print("\n3. 测试数据存储...")
    storage = Storage()
    success = storage.batch_store(nodes)
    print(f"数据存储{'成功' if success else '失败'}")
    
    # 验证存储
    test_node = storage.get(nodes[0].id)
    if test_node:
        print(f"验证存储: 成功读取节点 {test_node.id[:8]}")
    
    # 4. 测试索引构建
    print("\n4. 测试索引构建...")
    indexer = ESIndexer()
    
    # 创建索引
    print("创建文本索引...")
    indexer.create_literal_index()
    print("创建向量索引...")
    indexer.create_vector_index()
    
    # 索引文档
    print("索引文本文档...")
    indexer.index_literal_documents(nodes)
    print("索引向量文档...")
    indexer.index_vector_documents(nodes)
    
    # 5. 测试检索
    print("\n5. 测试检索...")
    retriever = ESRetriever()
    
    # 测试文本检索
    print("\n测试文本检索:")
    query = "金融科技的主要内容包括哪些"
    results = retriever.literal_search(query)
    print(f"文本检索结果数量: {len(results)}")
    if results:
        print("Top result:")
        print(f"Score: {results[0]['_score']}")
        print(f"Text: {results[0]['_source']['text'][:100]}...")
    
    # 测试向量检索
    print("\n测试向量检索:")
    results = retriever.vector_search(query)
    print(f"向量检索结果数量: {len(results)}")
    if results:
        print("Top result:")
        print(f"Score: {results[0]['_score']}")
        print(f"Text: {results[0]['_source']['text'][:100]}...")
    

    # except Exception as e:
    #     logger.error(f"测试文档处理流程失败: {e}")
    #     return False

if __name__ == "__main__":
    test_document_processing() 