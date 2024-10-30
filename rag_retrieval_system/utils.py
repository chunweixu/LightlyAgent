import os
import logging
import yaml
import config
from http import HTTPStatus
import dashscope

dashscope.api_key = config.LLM_KEY

# 日志工具
def setup_logger(name, log_file, level=logging.INFO):
    """创建并配置日志工具"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = setup_logger('rag_system', os.path.abspath(config.log_file))

def llm(content):
    messages = [{'role': 'user', 'content': content}]
    responses = dashscope.Generation.call(
        "qwen2-7b-instruct",
        messages=messages,
        result_format='message',  # set the result to be "message" format.
        stream=True,  # set streaming output
        incremental_output=True  # get streaming output incrementally
    )
    
    response_content = ""  # 初始化一个空字符串来收集输出
    
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            output_text = response.output.choices[0]['message']['content']
            response_content += output_text  # 将内容追加到response_content中
        else:
            error_message = (
                'Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message)
            )
            logger.error(error_message)  # 记录错误信息到日志
            print(error_message)
    
    # logger.info(f"API call completed with content: {response_content}")  # 记录成功信息到日志
    return response_content  # 返回生成的内容

# Function to get prompt from YAML file
def get_prompt(prompt_type: str) -> str:
    with open("prompts.yaml", "r", encoding="utf-8") as file:
        prompts = yaml.safe_load(file)
    return prompts.get(prompt_type, "")


def llm_embed(text: str):
    # Implementation of embedding generation should be added her
    resp = dashscope.TextEmbedding.call(
        model=dashscope.TextEmbedding.Models.text_embedding_v2,
        input=text, dimension=512)
    if resp.status_code == HTTPStatus.OK:
        embedding = resp.output['embeddings'][0]['embedding']
        return embedding
    else:
        logger.error(resp)
        return []
