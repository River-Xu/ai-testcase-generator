from __future__ import annotations
import json
import os
import re
from typing import Optional, List
from dotenv import load_dotenv
from pydantic import ValidationError

from .schemas import TestCaseSuite, TestCase
from .prompts import SYSTEM_PROMPT, user_prompt

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore

def _env(name: str, default: str = "") -> str:
    v = os.getenv(name)
    return v if v is not None and v != "" else default

def _rule_based_fallback(requirement_text: str) -> TestCaseSuite:
    # A lightweight fallback so the project can demo without any API key.
    module = "通用"
    if "登录" in requirement_text:
        module = "登录"
    elif "注册" in requirement_text:
        module = "注册"
    elif "支付" in requirement_text:
        module = "支付"

    base_cases: List[TestCase] = []
    base_cases.append(TestCase(
        id="TC-001",
        module=module,
        title="基础正向流程成功",
        preconditions=["系统可用", "依赖服务正常（如有）"],
        steps=["根据需求输入有效参数/信息", "提交/确认操作"],
        expected=["操作成功", "返回成功提示或正确响应"],
        priority="P0",
        type="正向",
        tags=["功能"]
    ))
    base_cases.append(TestCase(
        id="TC-002",
        module=module,
        title="必填参数缺失/为空",
        preconditions=[],
        steps=["构造缺失必填字段的请求/输入", "提交/确认操作"],
        expected=["校验失败", "明确提示缺失字段", "系统不产生脏数据"],
        priority="P0",
        type="反向",
        tags=["校验", "异常"]
    ))
    base_cases.append(TestCase(
        id="TC-003",
        module=module,
        title="边界值：最小/最大长度与特殊字符",
        preconditions=[],
        steps=["分别构造最小长度、最大长度、超长、含特殊字符的输入", "提交/确认操作"],
        expected=["边界内通过，越界被拒绝", "提示清晰", "编码与存储正确"],
        priority="P1",
        type="边界",
        tags=["边界", "输入"]
    ))
    base_cases.append(TestCase(
        id="TC-004",
        module=module,
        title="权限/鉴权：未登录或无权限访问",
        preconditions=[],
        steps=["在未登录或无权限状态下发起操作/请求"],
        expected=["拒绝访问", "返回 401/403 或等价提示", "无敏感信息泄露"],
        priority="P0",
        type="权限",
        tags=["鉴权", "安全"]
    ))
    base_cases.append(TestCase(
        id="TC-005",
        module=module,
        title="并发/重复提交提示",
        preconditions=[],
        steps=["短时间内重复提交同一请求/重复点击按钮（模拟并发）"],
        expected=["系统应幂等或做去重处理", "数据不重复", "响应稳定"],
        priority="P2",
        type="性能",
        tags=["幂等", "并发"]
    ))

    summary = "基于需求文本生成的通用测试用例集合（规则引擎 fallback）。"
    return TestCaseSuite(requirement_summary=summary, cases=base_cases)

def _try_llm(requirement_text: str) -> Optional[TestCaseSuite]:
    load_dotenv()
    api_key = _env("OPENAI_API_KEY", "")
    if not api_key or OpenAI is None:
        return None

    base_url = _env("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = _env("OPENAI_MODEL", "gpt-4o-mini")
    temperature = float(_env("TEMPERATURE", "0.2"))
    max_tokens = int(_env("MAX_TOKENS", "1500"))

    client = OpenAI(api_key=api_key, base_url=base_url)
    prompt = user_prompt(requirement_text)

    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    content = resp.choices[0].message.content or ""
    # Some models may wrap JSON in ```json fences.
    content = re.sub(r"^```json\s*|```\s*$", "", content.strip(), flags=re.IGNORECASE | re.MULTILINE).strip()
    try:
        data = json.loads(content)
        suite = TestCaseSuite.model_validate(data)
        return suite
    except (json.JSONDecodeError, ValidationError):
        return None

def generate_testcases(requirement_text: str) -> TestCaseSuite:
    """Generate testcases using LLM if configured; otherwise use a rule-based fallback."""
    suite = _try_llm(requirement_text)
    if suite is not None:
        return suite
    return _rule_based_fallback(requirement_text)
