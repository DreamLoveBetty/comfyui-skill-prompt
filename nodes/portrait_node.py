"""
人像提示词生成节点
"""

from ..config import DEFAULT_API_BASE_URL, DEFAULT_API_KEY, DEFAULT_MODEL, AVAILABLE_MODELS
from ..core.prompt_engine import PromptEngine


class PortraitPromptNode:
    """人像提示词生成器"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "description": ("STRING", {
                    "multiline": True,
                    "default": "职业女性全身像，横向画幅"
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
                "gender": (["自动", "女性", "男性"], {"default": "自动"}),
                "ethnicity": (["自动", "东亚", "欧美", "南亚", "非洲"], {"default": "自动"}),
                "style": (["自动", "电影级", "写实", "梦幻", "赛博朋克"], {"default": "自动"}),
                "lighting": (["自动", "自然光", "电影光", "霓虹", "戏剧"], {"default": "自动"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompt_natural_en", "prompt_natural_cn", "prompt_json_en", "prompt_json_cn")
    FUNCTION = "generate"
    CATEGORY = "Skill Prompt/人像"

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
        gender: str = "自动",
        ethnicity: str = "自动",
        style: str = "自动",
        lighting: str = "自动"
    ):
        # 收集选项
        options = {
            "gender": gender,
            "ethnicity": ethnicity,
            "style": style,
            "lighting": lighting
        }

        # 创建引擎并生成
        engine = PromptEngine()
        try:
            result = engine.generate(
                user_input=description,
                domain="portrait",
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
