"""
艺术提示词生成节点
"""

from ..config import DEFAULT_API_BASE_URL, DEFAULT_API_KEY, DEFAULT_MODEL, AVAILABLE_MODELS
from ..core.prompt_engine import PromptEngine


class ArtPromptNode:
    """艺术提示词生成器"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "description": ("STRING", {
                    "multiline": True,
                    "default": "中国水墨画山水风景"
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
                "art_style": (["自动", "水墨画", "油画", "水彩", "插画", "超现实"], {"default": "自动"}),
                "technique": (["自动", "写意", "工笔", "厚涂", "薄涂", "留白"], {"default": "自动"}),
                "mood": (["自动", "宁静", "壮观", "神秘", "欢快", "忧郁"], {"default": "自动"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompt_natural_en", "prompt_natural_cn", "prompt_json_en", "prompt_json_cn")
    FUNCTION = "generate"
    CATEGORY = "Skill Prompt/艺术"

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
        art_style: str = "自动",
        technique: str = "自动",
        mood: str = "自动"
    ):
        options = {
            "art_style": art_style,
            "technique": technique,
            "mood": mood
        }

        engine = PromptEngine()
        try:
            result = engine.generate(
                user_input=description,
                domain="art",
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
