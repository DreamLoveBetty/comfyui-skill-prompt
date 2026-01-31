"""
常识知识库 - 提供人种特征、风格映射等专业知识
用于增强 LLM 生成的准确性和一致性
"""


class KnowledgeBase:
    """常识知识库"""

    # 人种 → 典型眼睛颜色
    ETHNICITY_TYPICAL_EYES = {
        'East_Asian': ['black', 'dark brown', 'brown'],
        'Southeast_Asian': ['dark brown', 'brown', 'black'],
        'South_Asian': ['dark brown', 'brown', 'black'],
        'European': ['blue', 'green', 'brown', 'hazel', 'grey'],
        'African': ['dark brown', 'black', 'brown'],
        'Middle_Eastern': ['brown', 'dark brown', 'hazel', 'black'],
        'Latin_American': ['brown', 'dark brown', 'hazel', 'green'],
    }

    # 人种 → 典型发色
    ETHNICITY_TYPICAL_HAIR = {
        'East_Asian': ['black', 'dark brown'],
        'Southeast_Asian': ['black', 'dark brown'],
        'South_Asian': ['black', 'dark brown'],
        'European': ['blonde', 'brown', 'black', 'red', 'auburn'],
        'African': ['black', 'dark brown'],
        'Middle_Eastern': ['black', 'dark brown', 'brown'],
        'Latin_American': ['black', 'dark brown', 'brown'],
    }

    # 导演风格 → 光影需求映射
    DIRECTOR_LIGHTING_STYLES = {
        'zhang_yimou': {
            'description': '张艺谋电影风格',
            'lighting_keywords': ['dramatic shadows', 'rim lighting', 'chiaroscuro', 'high contrast', 'volumetric light'],
            'color_palette': ['rich red', 'gold', 'deep shadows'],
            'mood': 'epic, theatrical, emotionally intense'
        },
        'wong_kar_wai': {
            'description': '王家卫电影风格',
            'lighting_keywords': ['neon glow', 'saturated colors', 'moody lighting', 'color bleeding'],
            'color_palette': ['cyan', 'magenta', 'warm yellow'],
            'mood': 'nostalgic, melancholic, romantic'
        },
        'tsui_hark': {
            'description': '徐克武侠风格',
            'lighting_keywords': ['dynamic lighting', 'flowing motion', 'misty atmosphere'],
            'color_palette': ['jade green', 'misty white', 'golden'],
            'mood': 'wuxia, martial arts, ethereal'
        },
        'cinematic': {
            'description': '电影级质感',
            'lighting_keywords': ['cinematic lighting', 'film grain', 'anamorphic lens flare', 'shallow DOF'],
            'color_palette': ['natural tones', 'film color grading'],
            'mood': 'professional, polished, theatrical'
        },
        'film_noir': {
            'description': '黑色电影',
            'lighting_keywords': ['low key lighting', 'high contrast', 'deep shadows', 'venetian blind shadows'],
            'color_palette': ['black', 'white', 'grey'],
            'mood': 'mysterious, dramatic, suspenseful'
        }
    }

    # 领域 → 核心元素类别
    DOMAIN_CATEGORIES = {
        'portrait': [
            'gender', 'ethnicity', 'age_range', 'eye_types', 'hair_colors', 'hair_styles',
            'skin_tones', 'skin_textures', 'face_shapes', 'makeup_styles',
            'clothing_styles', 'expressions', 'poses', 'lighting_techniques',
            'backgrounds', 'photography_techniques'
        ],
        'art': [
            'art_styles', 'techniques', 'color_palettes', 'compositions',
            'brush_strokes', 'textures', 'moods', 'subjects'
        ],
        'design': [
            'design_types', 'color_schemes', 'typography', 'layouts',
            'visual_effects', 'backgrounds', 'decorative_elements'
        ],
        'product': [
            'product_types', 'lighting_setups', 'backgrounds', 'angles',
            'compositions', 'materials', 'reflections'
        ],
        'video': [
            'camera_movements', 'transitions', 'effects', 'moods',
            'pacing', 'color_grading', 'lighting_techniques'
        ]
    }

    # 风格类型定义
    STYLE_TYPES = {
        'anime': {'type': 'art_style', 'affects': 'rendering', 'description': '动漫绘画风格'},
        'manga': {'type': 'art_style', 'affects': 'rendering', 'description': '漫画绘画风格'},
        'realistic': {'type': 'art_style', 'affects': 'rendering', 'description': '写实绘画风格'},
        'illustration': {'type': 'art_style', 'affects': 'rendering', 'description': '插画绘画风格'},
        'cyberpunk': {'type': 'atmosphere', 'affects': 'scene', 'description': '赛博朋克场景氛围'},
        'fantasy': {'type': 'atmosphere', 'affects': 'scene', 'description': '奇幻场景氛围'},
        'vintage': {'type': 'atmosphere', 'affects': 'scene', 'description': '复古场景氛围'},
        'wuxia': {'type': 'atmosphere', 'affects': 'scene', 'description': '武侠场景氛围'},
    }

    @classmethod
    def get_ethnicity_constraints(cls, ethnicity: str) -> dict:
        """获取人种相关的约束信息"""
        return {
            'typical_eyes': cls.ETHNICITY_TYPICAL_EYES.get(ethnicity, ['brown']),
            'typical_hair': cls.ETHNICITY_TYPICAL_HAIR.get(ethnicity, ['black']),
            'ethnicity': ethnicity
        }

    @classmethod
    def get_director_style_info(cls, style: str) -> dict:
        """获取导演风格信息"""
        return cls.DIRECTOR_LIGHTING_STYLES.get(style, {})

    @classmethod
    def get_domain_categories(cls, domain: str) -> list:
        """获取领域的核心类别列表"""
        return cls.DOMAIN_CATEGORIES.get(domain, [])

    @classmethod
    def build_constraints_prompt(cls, options: dict) -> str:
        """根据选项构建约束提示词"""
        constraints = []

        # 人种约束
        ethnicity = options.get('ethnicity')
        if ethnicity and ethnicity != '自动':
            ethnicity_key = cls._normalize_ethnicity(ethnicity)
            info = cls.get_ethnicity_constraints(ethnicity_key)
            constraints.append(
                f"人种: {ethnicity} - 典型眼睛颜色: {', '.join(info['typical_eyes'][:3])}; "
                f"典型发色: {', '.join(info['typical_hair'][:2])}"
            )

        # 导演风格约束
        style = options.get('style') or options.get('lighting')
        if style and style != '自动':
            style_key = cls._normalize_style(style)
            if style_key in cls.DIRECTOR_LIGHTING_STYLES:
                info = cls.DIRECTOR_LIGHTING_STYLES[style_key]
                constraints.append(
                    f"风格: {info['description']} - 光影: {', '.join(info['lighting_keywords'][:3])}; "
                    f"色调: {', '.join(info['color_palette'][:2])}; 氛围: {info['mood']}"
                )

        return '\n'.join(constraints) if constraints else ''

    @staticmethod
    def _normalize_ethnicity(value: str) -> str:
        """标准化人种值"""
        mapping = {
            '东亚': 'East_Asian',
            '欧美': 'European',
            '南亚': 'South_Asian',
            '非洲': 'African',
            '中东': 'Middle_Eastern',
            '拉美': 'Latin_American',
        }
        return mapping.get(value, value)

    @staticmethod
    def _normalize_style(value: str) -> str:
        """标准化风格值"""
        mapping = {
            '电影级': 'cinematic',
            '张艺谋': 'zhang_yimou',
            '王家卫': 'wong_kar_wai',
            '徐克': 'tsui_hark',
            '黑色电影': 'film_noir',
        }
        return mapping.get(value, value)
