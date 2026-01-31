"""
提示词生成引擎 - 增强版
整合 LLM 语义理解 + 本地元素数据库 + 常识知识库
"""

import os
import json
import sqlite3
from typing import Optional, List, Dict
from .llm_client import LLMClient
from .knowledge_base import KnowledgeBase
from .design_variables import DesignVariables


class PromptEngine:
    """增强版提示词生成引擎"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            from ..config import DB_PATH
            db_path = DB_PATH
        self.db_path = db_path
        self._conn = None

    @property
    def conn(self):
        """懒加载数据库连接"""
        if self._conn is None and os.path.exists(self.db_path):
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    # =========================================================================
    # 数据库查询方法
    # =========================================================================

    def get_elements_by_domain(self, domain: str, limit: int = 50) -> List[Dict]:
        """从数据库获取指定领域的高质量元素"""
        if not self.conn:
            return []

        cursor = self.conn.execute("""
            SELECT element_id, name, chinese_name, ai_prompt_template,
                   keywords, reusability_score, category_id
            FROM elements
            WHERE domain_id = ?
            ORDER BY reusability_score DESC
            LIMIT ?
        """, (domain, limit))

        return [dict(row) for row in cursor.fetchall()]

    def get_elements_by_category(self, domain: str, category: str, limit: int = 10) -> List[Dict]:
        """获取指定领域和类别的元素"""
        if not self.conn:
            return []

        cursor = self.conn.execute("""
            SELECT element_id, name, chinese_name, ai_prompt_template,
                   keywords, reusability_score, category_id
            FROM elements
            WHERE domain_id = ? AND category_id = ?
            ORDER BY reusability_score DESC
            LIMIT ?
        """, (domain, category, limit))

        return [dict(row) for row in cursor.fetchall()]

    def search_elements(self, keywords: List[str], domain: str = None, limit: int = 20) -> List[Dict]:
        """搜索匹配关键词的元素"""
        if not self.conn or not keywords:
            return []

        conditions = []
        params = []

        for kw in keywords:
            conditions.append("(keywords LIKE ? OR name LIKE ? OR chinese_name LIKE ? OR ai_prompt_template LIKE ?)")
            params.extend([f"%{kw}%", f"%{kw}%", f"%{kw}%", f"%{kw}%"])

        where_clause = " OR ".join(conditions)

        if domain:
            where_clause = f"domain_id = ? AND ({where_clause})"
            params.insert(0, domain)

        cursor = self.conn.execute(f"""
            SELECT element_id, name, chinese_name, ai_prompt_template,
                   keywords, reusability_score, category_id, domain_id
            FROM elements
            WHERE {where_clause}
            ORDER BY reusability_score DESC
            LIMIT ?
        """, params + [limit])

        return [dict(row) for row in cursor.fetchall()]

    def get_category_stats(self, domain: str) -> Dict[str, int]:
        """获取领域内各类别的元素数量"""
        if not self.conn:
            return {}

        cursor = self.conn.execute("""
            SELECT category_id, COUNT(*) as count
            FROM elements
            WHERE domain_id = ?
            GROUP BY category_id
            ORDER BY count DESC
        """, (domain,))

        return {row['category_id']: row['count'] for row in cursor.fetchall()}

    # =========================================================================
    # 元素上下文构建
    # =========================================================================

    def build_element_context(self, domain: str, options: dict = None) -> str:
        """
        构建元素上下文，用于增强 LLM 提示词

        从数据库提取相关元素，构建结构化的参考信息
        """
        context_parts = []

        # 1. 获取领域核心类别
        categories = KnowledgeBase.get_domain_categories(domain)
        if not categories:
            categories = self._get_categories_from_db(domain)

        # 2. 为每个类别获取样本元素
        for category in categories[:8]:  # 限制类别数量
            elements = self.get_elements_by_category(domain, category, limit=5)
            if elements:
                category_samples = []
                for elem in elements:
                    template = elem.get('ai_prompt_template', '')
                    if template and len(template) < 200:
                        category_samples.append(template)

                if category_samples:
                    context_parts.append(f"【{category}】: {'; '.join(category_samples[:3])}")

        # 3. 根据选项搜索特定元素
        if options:
            search_keywords = self._extract_search_keywords(options)
            if search_keywords:
                matched_elements = self.search_elements(search_keywords, domain, limit=10)
                if matched_elements:
                    matched_samples = []
                    for elem in matched_elements[:5]:
                        template = elem.get('ai_prompt_template', '')
                        if template:
                            matched_samples.append(f"{elem.get('chinese_name', elem['name'])}: {template[:80]}")

                    if matched_samples:
                        context_parts.append(f"\n【匹配选项的元素】:\n" + '\n'.join(matched_samples))

        # 4. 添加常识约束
        constraints = KnowledgeBase.build_constraints_prompt(options or {})
        if constraints:
            context_parts.append(f"\n【一致性约束】:\n{constraints}")

        # 5. 添加设计风格上下文（仅 design 领域）
        if domain == "design" and options:
            design_style = options.get("设计风格")
            if design_style and design_style != "自动":
                design_context = DesignVariables.build_context(design_style, lang="en")
                if design_context:
                    context_parts.append(f"\n【设计风格参考 ({design_style})】:\n{design_context}")

        return '\n'.join(context_parts)

    def _get_categories_from_db(self, domain: str) -> List[str]:
        """从数据库获取领域的类别列表"""
        if not self.conn:
            return []

        cursor = self.conn.execute("""
            SELECT DISTINCT category_id
            FROM elements
            WHERE domain_id = ?
        """, (domain,))

        return [row['category_id'] for row in cursor.fetchall()]

    def _extract_search_keywords(self, options: dict) -> List[str]:
        """从选项中提取搜索关键词"""
        keywords = []

        # 中文到英文的映射
        value_mapping = {
            '女性': 'female', '男性': 'male',
            '东亚': 'East_Asian', '欧美': 'European',
            '自然光': 'natural light', '电影光': 'cinematic lighting',
            '霓虹': 'neon', '戏剧': 'dramatic',
            '电影级': 'cinematic', '写实': 'realistic',
            '梦幻': 'ethereal', '赛博朋克': 'cyberpunk',
            '水墨画': 'ink wash', '油画': 'oil painting',
            '现代简约': 'modern minimal', '商务': 'business',
        }

        for key, value in options.items():
            if value and value != '自动':
                # 尝试映射
                mapped = value_mapping.get(value, value)
                if mapped:
                    keywords.append(mapped)
                    # 保留原始值作为备选
                    if mapped != value:
                        keywords.append(value)

        return keywords

    # =========================================================================
    # 主生成方法
    # =========================================================================

    def generate(
        self,
        user_input: str,
        domain: str,
        api_base_url: str,
        api_key: str,
        model: str,
        options: dict = None,
        output_natural_en: bool = True,
        output_natural_cn: bool = False,
        output_json_en: bool = False,
        output_json_cn: bool = False,
        enable_enhance: bool = True  # 新增：是否启用二次扩写
    ) -> dict:
        """
        增强版生成提示词（主入口）

        Args:
            user_input: 用户输入描述
            domain: 领域（portrait/art/design/product/video）
            api_base_url: API 地址
            api_key: API 密钥
            model: 模型名称
            options: 可选参数（性别、风格等）
            output_*: 输出开关
            enable_enhance: 是否启用扩写增强

        Returns:
            包含4种输出的字典
        """
        # 1. 构建元素上下文（从数据库）
        element_context = self.build_element_context(domain, options)

        # 2. 初始化 LLM 客户端
        llm = LLMClient(api_base_url, api_key, model)

        # 3. 调用 LLM 生成（带元素上下文）
        result = llm.generate_prompt(
            user_input=user_input,
            domain=domain,
            options=options or {},
            element_context=element_context,
            output_natural_en=output_natural_en,
            output_natural_cn=output_natural_cn,
            output_json_en=output_json_en,
            output_json_cn=output_json_cn,
            enable_enhance=enable_enhance  # 新增：传递扩写开关
        )

        return result

    def enhance_with_elements(self, prompt: str, domain: str, limit: int = 5) -> str:
        """用数据库元素增强提示词（可选功能）"""
        if not self.conn:
            return prompt

        # 获取高质量元素
        elements = self.get_elements_by_domain(domain, limit)

        if not elements:
            return prompt

        # 提取模板片段
        enhancements = []
        for elem in elements:
            template = elem.get('ai_prompt_template', '')
            if template and len(template) < 100:  # 只用短模板
                enhancements.append(template)

        if enhancements:
            return f"{prompt}, {', '.join(enhancements[:3])}"

        return prompt

    def validate_consistency(self, intent: dict, generated_prompt: str) -> List[Dict]:
        """
        验证生成结果的一致性

        检查人种-眼睛颜色、人种-发色等约束
        返回问题列表
        """
        issues = []

        # 检查人种约束
        ethnicity = intent.get('ethnicity') or intent.get('subject', {}).get('ethnicity')
        if ethnicity:
            ethnicity_key = KnowledgeBase._normalize_ethnicity(ethnicity)
            constraints = KnowledgeBase.get_ethnicity_constraints(ethnicity_key)

            prompt_lower = generated_prompt.lower()

            # 检查不合理的眼睛颜色
            if ethnicity_key == 'East_Asian':
                incompatible_eyes = ['green eyes', 'blue eyes', 'violet eyes']
                for eye in incompatible_eyes:
                    if eye in prompt_lower:
                        issues.append({
                            'type': 'ethnicity_eye_mismatch',
                            'severity': 'warning',
                            'message': f"东亚人通常不会有{eye}",
                            'suggestion': f"建议使用: {', '.join(constraints['typical_eyes'][:2])} eyes"
                        })

        return issues
