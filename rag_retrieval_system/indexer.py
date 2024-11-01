from typing import List, Dict
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from data_structs import Node
import config
import utils

class ESIndexer:
    """Elasticsearch索引构建"""
    def __init__(self):
        self.es = Elasticsearch(
            f"http://{config.es_host}:{config.es_port}", 
            verify_certs=False
        )
        
    def create_literal_index(self):
        """创建文本索引"""
        index_name = "literal_index"
        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)
        
        mapping = {
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "metadata": {"type": "object"}
                }
            }
        }
        success = self.es.indices.create(index=index_name, body=mapping)
        print(f"Literal index created: {success}")
        return success
    
    def create_vector_index(self, vector_dim: int = 512):
        """创建向量索引"""
        index_name = "vector_index"
        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)
        
        mapping = {
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "vector": {
                        "type": "dense_vector",
                        "dims": vector_dim
                    }
                }
            }
        }
        success = self.es.indices.create(index=index_name, body=mapping)
        print(f"Vector index created: {success}")
        return success

    def index_literal_documents(self, nodes: List[Node]) -> bool:
        """索引文本文档"""
        actions = []
        for node in nodes:
            action = {
                "_index": "literal_index",
                "text": node.text,
                "metadata": node.metadata
            }
            actions.append(action)
        
        try:
            success, _ = bulk(self.es, actions)
            print(f"Indexed {success} documents to literal index")
            return True
        except Exception as e:
            print(f"Indexing to literal index failed: {e}")
            return False

    # def index_vector_documents(self, nodes: List[Node]) -> bool:
    #     """索引向量文档"""
    #     actions = []
    #     for node in nodes:
    #         vector = utils.llm_embed(node.text)  # 使用现有的embedding函数
    #         if vector:
    #             action = {
    #                 "_index": "vector_index",
    #                 "text": node.text,
    #                 "vector": vector
    #             }
    #             actions.append(action)
        
    #     # try:
    #     success, _ = bulk(self.es, actions)
    #     print(f"Indexed {success} documents to vector index")
    #     return True
    #     # except Exception as e:
    #     #     print(f"Indexing to vector index failed: {e}")
    #     #     return False 

    def index_vector_documents(self, nodes: List[Node]) -> bool:
        """索引向量文档"""
        import numpy as np
        actions = []
        for node in nodes:
            vector = utils.llm_embed(node.text)  # 使用现有的embedding函数
            if vector:
                # 确保vector是列表类型且包含浮点数
                if isinstance(vector, (list, np.ndarray)):
                    vector = [float(v) for v in vector]  # 转换为浮点数列表
                    action = {
                        "_index": "vector_index",
                        "text": node.text,
                        "vector": vector
                    }
                    actions.append(action)
                else:
                    print(f"无效的向量格式: {type(vector)}")
                    continue
        
        try:
            success, failed = bulk(self.es, actions)
            print(f"成功索引 {success} 个文档到向量索引")
            return True
        except Exception as e:
            print(f"向量索引失败: {str(e)}")
            # 打印第一个失败的文档以供调试
            if actions:
                print(f"示例文档: {actions[0]}")
            return False