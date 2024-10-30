from dataclasses import dataclass, field
from typing import Dict, Set, Optional
import uuid

@dataclass
class Node:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    index_set: Set[str] = field(default_factory=set)
    metadata: Dict[str, str] = field(default_factory=dict)
    start: int = 0
    end: int = 0
    text: str = ''

@dataclass
class StructIndex:
    index_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    summary: Optional[str] = None
    table: Dict[str, Set[str]] = field(default_factory=dict)
