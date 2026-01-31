"""
视频提示词生成节点
"""

from ..config import DEFAULT_API_BASE_URL, DEFAULT_API_KEY, DEFAULT_MODEL, AVAILABLE_MODELS
from ..core.prompt_engine import PromptEngine


class VideoPromptNode:
    """视频提示词生成器"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "description": ("STRING", {
                    "multiline": True,
                    "default": "武侠场景，人物飞檐走壁"
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
                "camera_movement": (["自动", "推", "拉", "摇", "移", "跟", "升降", "环绕"], {"default": "自动"}),
                "transition": (["自动", "淡入淡出", "硬切", "溶解", "擦除", "缩放"], {"default": "自动"}),
                "mood": (["自动", "紧张", "平静", "欢快", "悲伤", "史诗"], {"default": "自动"}),
                "speed": (["自动", "正常", "慢动作", "快动作", "延时"], {"default": "自动"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompt_natural_en", "prompt_natural_cn", "prompt_json_en", "prompt_json_cn")
    FUNCTION = "generate"
    CATEGORY = "Skill Prompt/视频"

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
        camera_movement: str = "自动",
        transition: str = "自动",
        mood: str = "自动",
        speed: str = "自动"
    ):
        options = {
            "camera_movement": camera_movement,
            "transition": transition,
            "mood": mood,
            "speed": speed
        }

        engine = PromptEngine()
        try:
            result = engine.generate(
                user_input=description,
                domain="video",
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
