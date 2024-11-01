import os
from typing import Dict, List, Optional
from data_structs import Node
import pickle
from utils import logger

class Storage:
    """使用本地文件系统实现KV存储"""
    def __init__(self):
        # 确保存储目录存在
        self.storage_dir = os.path.join("data", "storage")
        os.makedirs(self.storage_dir, exist_ok=True)
    
    def _get_file_path(self, node_id: str) -> str:
        """获取节点存储路径"""
        return os.path.join(self.storage_dir, f"{node_id}.pkl")
    
    def store(self, node: Node) -> bool:
        """存储单个节点"""
        try:
            file_path = self._get_file_path(node.id)
            with open(file_path, 'wb') as f:
                pickle.dump(node, f)
            return True
        except Exception as e:
            logger.error(f"Store node failed: {e}")
            return False
    
    def batch_store(self, nodes: List[Node]) -> bool:
        """批量存储节点"""
        try:
            for node in nodes:
                success = self.store(node)
                if not success:
                    return False
            return True
        except Exception as e:
            logger.error(f"Batch store nodes failed: {e}")
            return False
    
    def get(self, node_id: str) -> Optional[Node]:
        """获取节点"""
        try:
            file_path = self._get_file_path(node_id)
            if not os.path.exists(file_path):
                return None
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            logger.error(f"Get node failed: {e}")
            return None
    
    def get_batch(self, node_ids: List[str]) -> List[Optional[Node]]:
        """批量获取节点"""
        try:
            return [self.get(node_id) for node_id in node_ids]
        except Exception as e:
            logger.error(f"Batch get nodes failed: {e}")
            return [None] * len(node_ids)

