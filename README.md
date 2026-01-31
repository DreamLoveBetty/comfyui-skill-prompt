# ComfyUI Skill Prompt

AI 驱动的专业提示词生成插件，为 ComfyUI 提供智能化的图像生成提示词支持。

## ✨ 特性

- 🎯 **多领域支持**：人像、艺术、设计、产品、视频五大领域
- 📚 **专业元素库**：内置 1246+ 专业描述元素
- 🎨 **设计变量系统**：支持"温馨可爱"和"现代简约"风格
- 🔄 **多格式输出**：支持自然语言（中/英）和 JSON 结构化格式
- 🚀 **增强模式**：智能扩写，自动丰富提示词细节
- 🔌 **OpenAI 兼容**：支持任意 OpenAI 兼容 API

## 📦 安装

### 1. 克隆仓库

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/DreamLoveBetty/comfyui-skill-prompt.git
```

### 2. 安装依赖

```bash
cd comfyui-skill-prompt
pip install -r requirements.txt
```

### 3. 配置代理服务（可选）

本插件兼容任意 OpenAI 格式 API。推荐使用 [Antigravity-Manager](https://github.com/vanch007/Antigravity-Manager) 作为代理服务，支持 Gemini 等模型的 OpenAI 格式转换。

### 4. 重启 ComfyUI

## 🎮 使用方法

在 ComfyUI 中添加节点，位于 `Skill Prompt` 分类下：

| 节点 | 说明 |
|---|---|
| Portrait Prompt | 人像提示词生成 |
| Art Prompt | 艺术绘画提示词 |
| Design Prompt | 平面设计提示词 |
| Product Prompt | 产品摄影提示词 |
| Video Prompt | 视频场景提示词 |

### 参数说明

| 参数 | 说明 |
|---|---|
| description | 用户输入的场景描述（中文即可） |
| api_base_url | OpenAI 兼容 API 地址 |
| api_key | API 密钥 |
| model | 使用的模型 |
| output_natural_en/cn | 输出自然语言格式 |
| output_json_en/cn | 输出 JSON 结构化格式 |
| enable_enhance | 启用增强扩写模式 |
| 设计风格 | (Design 节点) 温馨可爱 / 现代简约 |

## 📁 项目结构

```
comfyui-skill-prompt/
├── __init__.py              # 入口文件
├── config.py                # 配置文件
├── requirements.txt         # 依赖列表
├── core/
│   ├── llm_client.py        # LLM 客户端
│   ├── prompt_engine.py     # 提示词引擎
│   ├── knowledge_base.py    # 常识知识库
│   └── design_variables.py  # 设计变量系统
├── nodes/
│   ├── portrait_node.py     # 人像节点
│   ├── art_node.py          # 艺术节点
│   ├── design_node.py       # 设计节点
│   ├── product_node.py      # 产品节点
│   └── video_node.py        # 视频节点
└── data/
    └── elements.db          # 专业元素库 (1246+ 元素)
```

## 🔗 相关项目

本项目基于以下项目开发：

| 项目 | 说明 |
|---|---|
| [skill-prompt-generator](https://github.com/huangserva/skill-prompt-generator) | 原始提示词生成器项目，提供元素库和设计变量系统 |
| [Antigravity-Manager](https://github.com/vanch007/Antigravity-Manager) | 推荐的 API 代理服务，支持 Gemini 等模型的 OpenAI 格式转换 |

## 🙏 致谢

- 感谢 [skill-prompt-generator](https://github.com/huangserva/skill-prompt-generator) 提供的专业元素库和设计变量系统
- 感谢 [Antigravity-Manager](https://github.com/vanch007/Antigravity-Manager) 提供的 API 代理服务支持

## 📄 许可证

MIT License
