from dataclasses import dataclass, field
from typing import Set

@dataclass
class Config:
    es_host: str = "localhost"
    es_port: int = 9200
    faiss_index_path: str = "./faiss_index"
    chunk_size: int = 512
    overlap: int = 50
    index_types: Set[str] = field(default_factory=lambda: {"Original"})
    log_file: str = "project.log"
