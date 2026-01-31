"""
产品提示词生成节点
"""

from ..config import DEFAULT_API_BASE_URL, DEFAULT_API_KEY, DEFAULT_MODEL, AVAILABLE_MODELS
from ..core.prompt_engine import PromptEngine


class ProductPromptNode:
    """产品提示词生成器"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "description": ("STRING", {
                    "multiline": True,
                    "default": "奢华手表产品摄影"
                }),
                "api_base_url": ("STRING", {
                    "default": DEFAULT_API_BASE_URL,
                    "multiline": False
                }),
                "api_key": ("STRING", {
                    "default": DEFAULT_API_KEY,
                    "multiline": False
                }),
                "model": (AVAILABLE_MODELS, {
                    "default": DEFAULT_MODEL
                }),
                "output_natural_en": ("BOOLEAN", {"default": True}),
                "output_natural_cn": ("BOOLEAN", {"default": False}),
                "output_json_en": ("BOOLEAN", {"default": False}),
                "output_json_cn": ("BOOLEAN", {"default": False}),
                "enable_enhance": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "product_type": (["自动", "电子产品", "服装", "食品", "化妆品", "珠宝"], {"default": "自动"}),
                "style": (["自动", "商业", "电商", "奢华", "简约", "创意"], {"default": "自动"}),
                "lighting": (["自动", "棚拍", "自然光", "戏剧", "高调", "低调"], {"default": "自动"}),
                "background": (["自动", "纯色", "渐变", "场景", "透明", "纹理"], {"default": "自动"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompt_natural_en", "prompt_natural_cn", "prompt_json_en", "prompt_json_cn")
    FUNCTION = "generate"
    CATEGORY = "Skill Prompt/产品"

    def generate(
        self,
        description: str,
        api_base_url: str,
        api_key: str,
        model: str,
        output_natural_en: bool,
        output_natural_cn: bool,
        output_json_en: bool,
        output_json_cn: bool,
        enable_enhance: bool,
        product_type: str = "自动",
        style: str = "自动",
        lighting: str = "自动",
        background: str = "自动"
    ):
        options = {
            "product_type": product_type,
            "style": style,
            "lighting": lighting,
            "background": background
        }

        engine = PromptEngine()
        try:
            result = engine.generate(
                user_input=description,
                domain="product",
                api_base_url=api_base_url,
                api_key=api_key,
                model=model,
                options=options,
                output_natural_en=output_natural_en,
                output_natural_cn=output_natural_cn,
                output_json_en=output_json_en,
                output_json_cn=output_json_cn,
                enable_enhance=enable_enhance
            )
        finally:
            engine.close()

        return (
            result.get("prompt_natural_en", ""),
            result.get("prompt_natural_cn", ""),
            result.get("prompt_json_en", ""),
            result.get("prompt_json_cn", "")
        )
