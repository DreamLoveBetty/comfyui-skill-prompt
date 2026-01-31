# ComfyUI Skill Prompt 插件配置

# 默认 API 配置
DEFAULT_API_BASE_URL = "http://127.0.0.1:8045/v1"
DEFAULT_API_KEY = "sk-f10af991b2a547c2b61dcc7d1face6bc"
DEFAULT_MODEL = "gemini-3-pro-high"

# 可用模型列表
AVAILABLE_MODELS = [
    "gemini-3-flash",
    "gemini-3-pro-high",
    "claude-sonnet-4-5-thinking",
    "claude-opus-4-5-thinking"
]

# 数据库路径（相对于插件目录）
import os
PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PLUGIN_DIR, "data", "elements.db")

# 领域配置
DOMAINS = {
    "portrait": "人像",
    "art": "艺术",
    "design": "设计",
    "product": "产品",
    "video": "视频"
}
