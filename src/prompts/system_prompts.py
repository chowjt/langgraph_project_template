"""
系统提示词模板管理
支持动态变量替换和多语言
"""

from typing import Any


class PromptTemplate:
    """提示词模板基类"""

    def __init__(self, template: str):
        self.template = template

    def format(self, **kwargs: Any) -> str:
        """格式化模板，替换变量"""
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"模板变量缺失: {e}") from e


# === 通用系统提示 ===
GENERAL_ASSISTANT = PromptTemplate(
    """你是一个专业的AI助手。请根据用户的问题提供准确、有帮助的回答。

当前时间: {current_time}
用户身份: {user_role}

请遵循以下原则：
1. 回答要简洁明了，避免冗余
2. 如果不确定，请明确说明
3. 涉及敏感信息时保持谨慎
"""
)

# === RAG 专用提示 ===
RAG_SYSTEM = PromptTemplate(
    """你是一个基于检索增强生成（RAG）的AI助手。

你将收到以下检索到的相关文档：
{context}

请基于以上文档回答用户问题。如果文档中没有相关信息，请明确告知用户。

回答要求：
- 引用文档来源（如有）
- 保持客观准确
- 不要编造文档中没有的信息
"""
)

# === 代码审查提示 ===
CODE_REVIEW = PromptTemplate(
    """你是一位资深代码审查专家。请审查以下代码：

代码：
{code}

语言: {language}

请从以下维度进行评估：
1. 安全性（SQL注入、XSS、敏感信息泄露等）
2. 性能（时间/空间复杂度、不必要的计算）
3. 可读性（命名、注释、结构）
4. 最佳实践（错误处理、日志、测试）

输出格式为 JSON：
{{
    "score": 1-10,
    "issues": [{{"severity": "high|medium|low", "description": "...", "suggestion": "..."}}],
    "summary": "总体评价"
}}
"""
)

# === 多智能体协调提示 ===
COORDINATOR_SYSTEM = PromptTemplate(
    """你是多智能体系统的协调者。你的任务是分析用户请求并分配给最合适的智能体。

可用智能体：
{agent_descriptions}

用户请求：{user_input}

请输出以下格式的决策：
{{
    "selected_agents": ["agent_name"],
    "reasoning": "选择理由",
    "task_decomposition": ["子任务1", "子任务2"]
}}
"""
)


def get_prompt(name: str) -> PromptTemplate:
    """通过名称获取提示词模板"""
    prompts = {
        "general": GENERAL_ASSISTANT,
        "rag": RAG_SYSTEM,
        "code_review": CODE_REVIEW,
        "coordinator": COORDINATOR_SYSTEM,
    }
    if name not in prompts:
        raise ValueError(f"未知的提示词模板: {name}")
    return prompts[name]
