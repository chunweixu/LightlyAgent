from typing import List, Dict
from elasticsearch import Elasticsearch
import config
import utils

class ESRetriever:
    """Elasticsearch检索实现"""
    def __init__(self):
        self.es = Elasticsearch(
            f"http://{config.es_host}:{config.es_port}", 
            verify_certs=False
        )
    
    def literal_search(self, query: str, top_k: int = 10) -> List[Dict]:
        """文本检索"""
        try:
            response = self.es.search(
                index="literal_index",
                body={
                    "query": {
                        "match": {
                            "text": query
                        }
                    },
                    "size": top_k
                }
            )
            return response['hits']['hits']
        except Exception as e:
            print(f"Literal search failed: {e}")
            return []

    def vector_search(self, query: str, top_k: int = 10) -> List[Dict]:
        """向量检索"""
        try:
            # 生成查询向量
            query_vector = utils.llm_embed(query)
            if not query_vector:
                return []
            
            response = self.es.search(
                index="vector_index",
                body={
                    "query": {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                                "params": {"query_vector": query_vector}
                            }
                        }
                    },
                    "size": top_k
                }
            )
            return response['hits']['hits']
        except Exception as e:
            print(f"Vector search failed: {e}")
            return []

    def hybrid_search(self, query: str, top_k: int = 10) -> List[Dict]:
        """混合检索"""
        try:
            # 获取两种检索结果
            literal_results = self.literal_search(query, top_k)
            vector_results = self.vector_search(query, top_k)
            
            # 简单的结果合并和排序
            all_results = {}
            
            # 处理文本检索结果
            for hit in literal_results:
                text = hit['_source']['text']
                all_results[text] = {
                    'text': text,
                    'literal_score': hit['_score'],
                    'vector_score': 0
                }
            
            # 处理向量检索结果
            for hit in vector_results:
                text = hit['_source']['text']
                if text in all_results:
                    all_results[text]['vector_score'] = hit['_score']
                else:
                    all_results[text] = {
                        'text': text,
                        'literal_score': 0,
                        'vector_score': hit['_score']
                    }
            
            # 计算综合得分并排序
            results = list(all_results.values())
            results.sort(key=lambda x: x['literal_score'] + x['vector_score'], reverse=True)
            
            return results[:top_k]
        except Exception as e:
            print(f"Hybrid search failed: {e}")
            return [] 