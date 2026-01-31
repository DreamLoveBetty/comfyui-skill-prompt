"""
设计提示词生成节点
"""

from ..config import DEFAULT_API_BASE_URL, DEFAULT_API_KEY, DEFAULT_MODEL, AVAILABLE_MODELS
from ..core.prompt_engine import PromptEngine


class DesignPromptNode:
    """设计提示词生成器"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "description": ("STRING", {
                    "multiline": True,
                    "default": "现代简约科技风格海报"
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
                "design_type": (["自动", "海报", "UI", "卡片", "Logo", "Banner"], {"default": "自动"}),
                "设计风格": (["自动", "温馨可爱", "现代简约"], {"default": "自动"}),
                "color_scheme": (["自动", "明亮", "暗色", "渐变", "单色", "互补色"], {"default": "自动"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompt_natural_en", "prompt_natural_cn", "prompt_json_en", "prompt_json_cn")
    FUNCTION = "generate"
    CATEGORY = "Skill Prompt/设计"

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
        design_type: str = "自动",
        设计风格: str = "自动",
        color_scheme: str = "自动"
    ):
        options = {
            "design_type": design_type,
            "设计风格": 设计风格,
            "color_scheme": color_scheme
        }

        engine = PromptEngine()
        try:
            result = engine.generate(
                user_input=description,
                domain="design",
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
