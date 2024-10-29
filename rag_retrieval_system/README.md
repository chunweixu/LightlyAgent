# RAG 检索系统

## 概述
RAG（检索增强生成）检索系统是一个模块化项目，集成了多种技术，用于解析文档、生成索引以及使用 Elasticsearch 和 Faiss 检索相关段落。该系统由多个组件组成，它们共同提供灵活高效的自然语言查询检索解决方案。

## 项目结构
```
/rag_retrieval_system
    ├── data_parser.py         # 数据解析与段落切分模块
    ├── index.py               # 索引生成和 Elasticsearch/Faiss 索引构建模块
    ├── retrieval.py           # 多通道检索模块
    ├── fusion_ranker.py       # 融合排序模块，用于合并检索结果
    ├── paragraph_mapper.py    # 用于映射索引到原始段落并去重的模块
    ├── main.py                # 主程序，控制整个工作流程
    ├── app.py                 # 使用 Streamlit 进行可视化和交互
    ├── data_structs.py        # Node 和 StructIndex 数据结构定义
    ├── config.py              # 配置信息
    └── utils.py               # 公共函数，包括日志设置
```

## 安装
1. **克隆代码库**
    ```bash
    git clone <repository_url>
    cd rag_retrieval_system
    ```

2. **安装依赖**
    确保安装了 Python 3.8 以上版本。使用以下命令安装所需的 Python 包：
    ```bash
    pip install -r requirements.txt
    ```

3. **设置 Elasticsearch 和 Faiss**
    - 确保在本地安装并运行了 Elasticsearch。
    - 安装 Faiss Python 包：
    ```bash
    pip install faiss-cpu
    ```

## 配置
修改 `config.py` 文件，设置 Elasticsearch 主机、端口、段大小、重叠等参数。

```python
@dataclass
class Config:
    es_host: str = "localhost"
    es_port: int = 9200
    faiss_index_path: str = "./faiss_index"
    chunk_size: int = 512
    overlap: int = 50
    index_types: Set[str] = field(default_factory=lambda: {"Original"})
    log_file: str = "project.log"
```

## 使用方法
### 1. 运行主工作流
主工作流在 `main.py` 中实现，集成了从数据解析、索引生成、检索到去重的整个流程。

```bash
python main.py
```

该脚本将执行以下步骤：
- 解析文档并将其分段。
- 为每个段生成索引。
- 构建 Elasticsearch 和 Faiss 索引。
- 为示例查询检索结果。
- 应用融合排序。
- 映射并去重结果。

### 2. 运行 Streamlit 应用
您还可以使用 Streamlit 应用来可视化并与 RAG 系统交互。

```bash
streamlit run app.py
```
