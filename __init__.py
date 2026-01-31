"""
ComfyUI Skill Prompt 插件
智能提示词生成器 - 支持人像/艺术/设计/产品/视频 5大领域
"""

from .nodes.portrait_node import PortraitPromptNode
from .nodes.art_node import ArtPromptNode
from .nodes.design_node import DesignPromptNode
from .nodes.product_node import ProductPromptNode
from .nodes.video_node import VideoPromptNode

# ComfyUI 节点注册
NODE_CLASS_MAPPINGS = {
    "PortraitPromptNode": PortraitPromptNode,
    "ArtPromptNode": ArtPromptNode,
    "DesignPromptNode": DesignPromptNode,
    "ProductPromptNode": ProductPromptNode,
    "VideoPromptNode": VideoPromptNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PortraitPromptNode": "🎭 人像提示词生成器",
    "ArtPromptNode": "🎨 艺术提示词生成器",
    "DesignPromptNode": "📐 设计提示词生成器",
    "ProductPromptNode": "📦 产品提示词生成器",
    "VideoPromptNode": "🎬 视频提示词生成器",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

print("\033[92m[Skill Prompt] 插件加载成功！5个领域节点已注册。\033[0m")
