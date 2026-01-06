SYSTEM_PROMPT = """你是资深测试专家与AI应用工程师。
你将根据输入的需求描述，生成覆盖面广且可执行的测试用例，并以严格 JSON 输出。
要求：
- 覆盖：正向/反向/边界/异常/权限/安全（如适用）/性能提示（如适用）
- 用例可执行：步骤清晰、期望明确
- 结构化字段：id, module, title, preconditions, steps, expected, priority, type, tags
- 只输出 JSON，不要输出多余解释文字
"""

def user_prompt(requirement_text: str) -> str:
    return f"""需求描述如下（可能为中文/英文/混合）：
---
{requirement_text}
---

请输出 JSON，结构如下：
{{
  "requirement_summary": "...",
  "cases": [
    {{
      "id": "TC-001",
      "module": "模块名",
      "title": "用例标题",
      "preconditions": ["..."],
      "steps": ["..."],
      "expected": ["..."],
      "priority": "P0|P1|P2|P3",
      "type": "正向|反向|边界|异常|权限|安全|性能|兼容性|其他",
      "tags": ["..."]
    }}
  ]
}}
""".strip()
