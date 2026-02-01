"""
LLM 客户端 - 增强版
封装 OpenAI 兼容 API 调用，支持元素库上下文增强
"""

import json
from openai import OpenAI


class LLMClient:
    """增强版 LLM 客户端"""

    def __init__(self, base_url: str, api_key: str, model: str):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        self.model = model

    def generate_prompt(
        self,
        user_input: str,
        domain: str,
        options: dict,
        element_context: str = "",  # 元素上下文
        output_natural_en: bool = True,
        output_natural_cn: bool = False,
        output_json_en: bool = False,
        output_json_cn: bool = False,
        enable_enhance: bool = True  # 新增：是否启用二次扩写
    ) -> dict:
        """
        生成提示词（支持4种输出格式）

        Args:
            user_input: 用户输入描述
            domain: 领域
            options: 用户选项
            element_context: 元素库上下文（来自数据库）
            output_*: 输出格式开关

        Returns:
            包含4种输出格式的字典
        """

        # 构建输出要求
        output_requirements = []
        if output_natural_en:
            output_requirements.append("natural_en: 英文自然语言提示词（逗号分隔的关键词短语）")
        if output_natural_cn:
            output_requirements.append("natural_cn: 中文自然语言提示词（逗号分隔的关键词短语）")
        if output_json_en:
            output_requirements.append("json_en: 英文JSON结构化提示词")
        if output_json_cn:
            output_requirements.append("json_cn: 中文JSON结构化提示词")

        if not output_requirements:
            return {
                "prompt_natural_en": "",
                "prompt_natural_cn": "",
                "prompt_json_en": "",
                "prompt_json_cn": ""
            }

        # 构建增强版系统提示词
        system_prompt = self._build_enhanced_system_prompt(
            domain, output_requirements, options, element_context, enable_enhance
        )

        # 根据模型类型动态设置参数
        model_lower = self.model.lower()
        
        # 构建请求参数
        request_params = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "stream": True
        }
        
        # Claude Thinking 模型：不传递 max_tokens 和 temperature（使用代理默认值）
        # Gemini 模型：使用 8192
        # 其他模型：使用 16384
        if 'thinking' in model_lower:
            # Claude Thinking 模型使用代理默认值
            pass
        elif 'gemini' in model_lower:
            request_params["max_tokens"] = 8192
            request_params["temperature"] = 0.8
        else:
            request_params["max_tokens"] = 16384
            request_params["temperature"] = 0.8

        # 使用流式传输增加稳定性（避免大模型超时）
        response = self.client.chat.completions.create(**request_params)

        # 收集流式响应
        content = self._collect_stream_response(response)
        return self._parse_generation_response(
            content,
            output_natural_en,
            output_natural_cn,
            output_json_en,
            output_json_cn
        )

    def _collect_stream_response(self, stream) -> str:
        """
        收集流式响应并拼接完整内容

        Args:
            stream: OpenAI 流式响应迭代器

        Returns:
            完整的响应文本
        """
        collected_content = []

        for chunk in stream:
            # 检查 chunk 是否有内容
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    collected_content.append(delta.content)

        return ''.join(collected_content)

    def _build_enhanced_system_prompt(
        self,
        domain: str,
        output_requirements: list,
        options: dict,
        element_context: str,
        enable_enhance: bool = True
    ) -> str:
        """构建增强版系统提示词（包含元素库知识 + 扩写规则）"""

        domain_descriptions = {
            "portrait": "人像摄影",
            "art": "艺术绘画",
            "design": "平面设计",
            "product": "产品摄影",
            "video": "视频场景"
        }

        domain_desc = domain_descriptions.get(domain, "通用")

        # 构建选项描述
        options_desc = ""
        if options:
            valid_options = {k: v for k, v in options.items() if v and v != "自动"}
            if valid_options:
                options_desc = f"\n【用户指定选项】：{json.dumps(valid_options, ensure_ascii=False)}"

        outputs_str = "\n".join(f"- {req}" for req in output_requirements)

        # 构建元素库参考部分
        element_reference = ""
        if element_context:
            element_reference = f"""

## 专业元素库参考（请优先使用这些专业描述）：
{element_context}

⚠️ 重要：请基于上述专业元素库中的描述来生成提示词，确保使用专业、准确的术语。"""

        # 扩写增强规则
        enhance_rules = ""
        if enable_enhance:
            enhance_rules = self._build_enhance_rules(domain)

        return f"""你是专业的{domain_desc}提示词生成专家。

根据用户描述生成高质量的AI图像生成提示词。{options_desc}
{element_reference}
{enhance_rules}

## 生成要求：

### 一致性规则（必须遵守）：
1. 人种与眼睛颜色一致：东亚人应使用 dark brown eyes / almond eyes，不要使用 green/blue eyes
2. 人种与发色一致：东亚人通常使用 black hair / dark brown hair
3. 时代与服装一致：古装场景使用 traditional/period 服装，现代场景使用 modern/contemporary 服装
4. 风格与光影匹配：电影级风格使用 cinematic lighting, dramatic shadows；自然风格使用 soft natural light

### 输出格式：
{outputs_str}

### 格式规范：
1. 使用 === natural_en === 等分隔符标记每个部分
2. 自然语言格式：逗号分隔的描述性短语，详细丰富，包含主体、风格、光影、构图、技术参数等
3. JSON格式：结构化的键值对，包含 subject/styling/lighting/scene/technical 等分类

### 示例输出格式：
=== natural_en ===
professional Asian woman, full body shot, business formal attire, dark brown almond eyes, sleek black hair, natural makeup, soft window light, shallow depth of field, 85mm lens, 8K resolution

=== natural_cn ===
职业亚洲女性，全身照，商务正装，深棕色杏仁眼，黑色直发，自然妆容，柔和窗光，浅景深，85mm镜头，8K分辨率

=== json_en ===
{{"subject": {{"gender": "female", "ethnicity": "East Asian", "age": "adult"}}, "styling": {{"clothing": "business formal", "hair": "black sleek", "makeup": "natural"}}, "lighting": {{"type": "window light", "mood": "soft professional"}}, "technical": {{"lens": "85mm", "resolution": "8K"}}}}

=== json_cn ===
{{"主体": {{"性别": "女性", "人种": "东亚", "年龄": "成年"}}, "造型": {{"服装": "商务正装", "发型": "黑色直发", "妆容": "自然"}}, "光影": {{"类型": "窗光", "氛围": "柔和职业感"}}, "技术": {{"镜头": "85mm", "分辨率": "8K"}}}}

请生成详细、专业、符合一致性规则的提示词。"""

    def _parse_generation_response(
        self,
        content: str,
        output_natural_en: bool,
        output_natural_cn: bool,
        output_json_en: bool,
        output_json_cn: bool
    ) -> dict:
        """解析生成响应"""
        result = {
            "prompt_natural_en": "",
            "prompt_natural_cn": "",
            "prompt_json_en": "",
            "prompt_json_cn": ""
        }

        # 解析各个部分
        if output_natural_en and "=== natural_en ===" in content:
            try:
                part = content.split("=== natural_en ===")[1]
                if "===" in part:
                    part = part.split("===")[0]
                result["prompt_natural_en"] = part.strip()
            except:
                pass

        if output_natural_cn and "=== natural_cn ===" in content:
            try:
                part = content.split("=== natural_cn ===")[1]
                if "===" in part:
                    part = part.split("===")[0]
                result["prompt_natural_cn"] = part.strip()
            except:
                pass

        if output_json_en and "=== json_en ===" in content:
            try:
                part = content.split("=== json_en ===")[1]
                if "===" in part:
                    part = part.split("===")[0]
                # 清理 JSON
                part = part.strip()
                if "```json" in part:
                    part = part.split("```json")[1].split("```")[0]
                elif "```" in part:
                    part = part.split("```")[1].split("```")[0]
                result["prompt_json_en"] = part.strip()
            except:
                pass

        if output_json_cn and "=== json_cn ===" in content:
            try:
                part = content.split("=== json_cn ===")[1]
                if "===" in part:
                    part = part.split("===")[0]
                part = part.strip()
                if "```json" in part:
                    part = part.split("```json")[1].split("```")[0]
                elif "```" in part:
                    part = part.split("```")[1].split("```")[0]
                result["prompt_json_cn"] = part.strip()
            except:
                pass

        # 如果解析失败，尝试直接使用内容
        if output_natural_en and not result["prompt_natural_en"]:
            # 没有分隔符，假设整个内容是自然语言英文
            if "===" not in content:
                result["prompt_natural_en"] = content.strip()

        return result

    def _build_enhance_rules(self, domain: str) -> str:
        """
        构建领域扩写规则（LLM 自主推理维度）
        
        不再硬编码扩写维度，让 LLM 根据上下文自主推理最适合的扩写方向
        """
        # 领域名称映射
        domain_name = {
            "portrait": "人像摄影",
            "art": "艺术绘画",
            "design": "平面设计",
            "product": "产品摄影",
            "video": "视频场景"
        }.get(domain, "通用")
        
        return f"""

## 扩写增强规则（必须遵守）：

### 扩写维度：
请根据上述【用户描述】和【{domain_name}】领域特点，根据输入复杂度自主推理出 **3-8 个**最适合本次生成的扩写维度（如：服饰、发型、姿势、背景、神态、表情、动作、材质、光影、氛围、动态、质感、构图、色调等），并按这些维度丰富提示词细节。

### 长度控制：
- 自然语言输出：控制在 **600-800 字符**
- JSON 输出：控制在 **1000-1200 字符**

### 扩写规范：
1. **只增不改**：在核心描述基础上追加细节修饰，保持原始语义不变
2. **语义去重**：避免隐含重复（如"黑丝袜"已含"丝袜"概念，不再重复 stockings）
3. **关键元素前置**：主体关键描述放在**前 150 字符**内，确保核心元素获得最高权重
4. **层次递进**：从主体→环境→氛围→技术参数，由近及远、由主及次
"""
