"""
设计变量模块 - 从原项目提取的有价值设计元素
仅保留图像生成模型可理解的内容（颜色名称、风格关键词、装饰概念）
"""

import random
from typing import Dict, List, Optional


class DesignVariables:
    """轻量级设计变量，用于增强 design 领域的提示词"""

    # =========================================================================
    # 颜色调色板（去除 CSS 参数，只保留颜色名称）
    # =========================================================================
    COLOR_PALETTES = {
        "温馨可爱": {
            "珊瑚粉色系": {
                "en": ["peach pink", "light coral", "soft peach", "light pink", "rose pink"],
                "cn": ["蜜桃粉", "浅珊瑚", "桃子白", "浅粉红", "玫瑰粉"],
            },
            "天空蓝色系": {
                "en": ["sky blue", "light periwinkle", "mint blue", "fresh green", "pale mint"],
                "cn": ["天空蓝", "淡紫蓝", "薄荷蓝", "清新绿", "淡薄荷"],
            },
            "薄荷绿色系": {
                "en": ["mint green", "tender grass green", "spring green", "fresh green"],
                "cn": ["薄荷绿", "嫩草绿", "春绿色", "清新绿"],
            },
            "奶油色系": {
                "en": ["cream white", "vanilla white", "peach white", "lemon white", "apricot white"],
                "cn": ["奶油白", "香草白", "桃子白", "柠檬白", "杏子白"],
            },
        },
        "现代简约": {
            "深蓝色系": {
                "en": ["deep charcoal blue", "rock blue", "medium blue gray"],
                "cn": ["深炭蓝", "岩石蓝", "中蓝灰"],
            },
            "靛蓝色系": {
                "en": ["indigo", "purple", "light purple"],
                "cn": ["靛蓝", "紫色", "淡紫"],
            },
            "深绿色系": {
                "en": ["deep green", "emerald green", "mint"],
                "cn": ["深绿", "翠绿", "薄荷"],
            },
            "中性灰系": {
                "en": ["deep gray", "medium gray", "light gray"],
                "cn": ["深灰", "中灰", "浅灰"],
            },
        },
    }

    # =========================================================================
    # 风格关键词（从 design-logic 提取）
    # =========================================================================
    STYLE_KEYWORDS = {
        "温馨可爱": {
            "atmosphere": {
                "en": ["warm", "soft", "cozy", "gentle", "playful", "dreamy", "whimsical"],
                "cn": ["温暖", "柔软", "温馨", "轻柔", "俏皮", "梦幻", "奇幻"],
            },
            "lighting": {
                "en": ["soft diffused light", "warm ambient glow", "dreamy lighting", "gentle illumination"],
                "cn": ["柔和漫射光", "温暖环境光", "梦幻光效", "轻柔照明"],
            },
            "texture": {
                "en": ["smooth", "fluffy", "plush", "soft", "rounded"],
                "cn": ["光滑", "蓬松", "毛绒", "柔软", "圆润"],
            },
            "decoration": {
                "en": ["sparkles", "hearts", "clouds", "flowers", "balloons", "stars", "ribbons"],
                "cn": ["星光", "爱心", "云朵", "花朵", "气球", "星星", "丝带"],
            },
        },
        "现代简约": {
            "atmosphere": {
                "en": ["professional", "clean", "minimal", "sophisticated", "elegant", "refined"],
                "cn": ["专业", "干净", "简约", "精致", "优雅", "精炼"],
            },
            "lighting": {
                "en": ["studio lighting", "subtle shadows", "even illumination", "soft ambient light"],
                "cn": ["工作室灯光", "微妙阴影", "均匀照明", "柔和环境光"],
            },
            "texture": {
                "en": ["sleek", "matte", "polished", "smooth", "flat"],
                "cn": ["光滑", "亚光", "抛光", "平滑", "扁平"],
            },
            "decoration": {
                "en": ["geometric lines", "dot patterns", "subtle gradients", "minimal shapes"],
                "cn": ["几何线条", "点阵图案", "微妙渐变", "简约形状"],
            },
        },
    }

    # =========================================================================
    # 风格约束（设计原则：避免什么、偏好什么）
    # =========================================================================
    STYLE_CONSTRAINTS = {
        "温馨可爱": {
            "avoid": {
                "en": ["dark colors", "sharp edges", "harsh lighting", "cold tones", "complex patterns"],
                "cn": ["深色", "尖锐边缘", "强烈光照", "冷色调", "复杂图案"],
            },
            "prefer": {
                "en": ["pastel colors", "rounded shapes", "soft shadows", "warm tones", "simple cute elements"],
                "cn": ["粉彩色", "圆润形状", "柔和阴影", "暖色调", "简单可爱元素"],
            },
        },
        "现代简约": {
            "avoid": {
                "en": ["bright saturated colors", "excessive decoration", "playful elements", "cluttered layout"],
                "cn": ["鲜艳饱和色", "过度装饰", "俏皮元素", "杂乱布局"],
            },
            "prefer": {
                "en": ["neutral tones", "geometric shapes", "minimal decoration", "clean lines", "ample whitespace"],
                "cn": ["中性色调", "几何形状", "极简装饰", "干净线条", "充足留白"],
            },
        },
    }

    @classmethod
    def get_available_styles(cls) -> List[str]:
        """获取可用的设计风格列表"""
        return list(cls.STYLE_KEYWORDS.keys())

    @classmethod
    def sample_color_palette(cls, style: str, lang: str = "en") -> Optional[Dict]:
        """
        随机采样一个配色方案
        
        Args:
            style: 风格名称
            lang: 语言 ("en" 或 "cn")
        
        Returns:
            {"palette_name": "珊瑚粉色系", "colors": ["peach pink", ...]}
        """
        if style not in cls.COLOR_PALETTES:
            return None
        
        palettes = cls.COLOR_PALETTES[style]
        palette_name = random.choice(list(palettes.keys()))
        colors = palettes[palette_name].get(lang, [])
        
        return {
            "palette_name": palette_name,
            "colors": colors,
        }

    @classmethod
    def get_style_keywords(cls, style: str, lang: str = "en") -> Dict[str, List[str]]:
        """
        获取风格关键词
        
        Args:
            style: 风格名称
            lang: 语言
        
        Returns:
            {"atmosphere": [...], "lighting": [...], ...}
        """
        if style not in cls.STYLE_KEYWORDS:
            return {}
        
        result = {}
        for category, translations in cls.STYLE_KEYWORDS[style].items():
            result[category] = translations.get(lang, [])
        
        return result

    @classmethod
    def get_style_constraints(cls, style: str, lang: str = "en") -> Dict[str, List[str]]:
        """获取风格约束（避免/偏好）"""
        if style not in cls.STYLE_CONSTRAINTS:
            return {}
        
        result = {}
        for constraint_type, translations in cls.STYLE_CONSTRAINTS[style].items():
            result[constraint_type] = translations.get(lang, [])
        
        return result

    @classmethod
    def build_context(cls, style: str, lang: str = "en") -> str:
        """
        构建设计上下文字符串，用于增强 LLM 提示词
        
        Args:
            style: 风格名称
            lang: 语言
        
        Returns:
            格式化的上下文字符串
        """
        if style not in cls.STYLE_KEYWORDS:
            return ""
        
        parts = []
        
        # 1. 配色参考
        palette = cls.sample_color_palette(style, lang)
        if palette:
            colors_str = ", ".join(palette["colors"][:4])
            if lang == "en":
                parts.append(f"Color palette ({palette['palette_name']}): {colors_str}")
            else:
                parts.append(f"配色方案（{palette['palette_name']}）：{colors_str}")
        
        # 2. 风格关键词
        keywords = cls.get_style_keywords(style, lang)
        if keywords:
            if lang == "en":
                parts.append(f"Atmosphere: {', '.join(keywords.get('atmosphere', [])[:4])}")
                parts.append(f"Lighting: {', '.join(keywords.get('lighting', [])[:2])}")
                parts.append(f"Decoration elements: {', '.join(keywords.get('decoration', [])[:4])}")
            else:
                parts.append(f"氛围：{', '.join(keywords.get('atmosphere', [])[:4])}")
                parts.append(f"光影：{', '.join(keywords.get('lighting', [])[:2])}")
                parts.append(f"装饰元素：{', '.join(keywords.get('decoration', [])[:4])}")
        
        # 3. 偏好约束
        constraints = cls.get_style_constraints(style, lang)
        if constraints and constraints.get("prefer"):
            if lang == "en":
                parts.append(f"Design preference: {', '.join(constraints['prefer'][:3])}")
            else:
                parts.append(f"设计偏好：{', '.join(constraints['prefer'][:3])}")
        
        return "\n".join(parts)

    @classmethod
    def build_prompt_enhancement(cls, style: str, lang: str = "en") -> str:
        """
        构建直接可用的提示词增强片段
        
        Args:
            style: 风格名称
            lang: 语言
        
        Returns:
            逗号分隔的提示词片段
        """
        if style not in cls.STYLE_KEYWORDS:
            return ""
        
        fragments = []
        
        # 采样配色
        palette = cls.sample_color_palette(style, lang)
        if palette and palette["colors"]:
            fragments.append(f"{palette['colors'][0]} color scheme")
        
        # 采样氛围词
        keywords = cls.get_style_keywords(style, lang)
        if keywords.get("atmosphere"):
            fragments.extend(random.sample(keywords["atmosphere"], min(2, len(keywords["atmosphere"]))))
        
        # 采样光影
        if keywords.get("lighting"):
            fragments.append(random.choice(keywords["lighting"]))
        
        # 采样装饰
        if keywords.get("decoration"):
            decorations = random.sample(keywords["decoration"], min(2, len(keywords["decoration"])))
            fragments.append(f"decorated with {' and '.join(decorations)}")
        
        return ", ".join(fragments)
