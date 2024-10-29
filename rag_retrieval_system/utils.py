import logging
from logging.handlers import RotatingFileHandler
import yaml

# Setup logger function
def setup_logger(name, log_file, level=logging.INFO):
    """创建并配置日志工具"""
    handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=2)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Function to get prompt from YAML file
def get_prompt(prompt_type: str) -> str:
    with open("prompts.yaml", "r", encoding="utf-8") as file:
        prompts = yaml.safe_load(file)
    return prompts.get(prompt_type, "")

# Placeholder LLM functions (implement according to your LLM API)
def llm(prompt: str) -> str:
    # Implementation of the LLM API call should be added here
    return "Generated response based on prompt"

def llm_embed(text: str):
    # Implementation of embedding generation should be added here
    return [0.1, 0.2, 0.3]  # Replace with actual embedding

# Create a global logger instance
from config import Config

config = Config()
logger = setup_logger('rag_system', config.log_file)
