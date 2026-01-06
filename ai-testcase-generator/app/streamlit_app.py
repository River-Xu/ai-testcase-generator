from __future__ import annotations
import streamlit as st
from aitestgen import generate_testcases, export_testcases
import tempfile
import os

st.set_page_config(page_title="AI Testcase Generator", layout="wide")

st.title("AI Testcase Generator（AI 测试用例生成器）")
st.caption("输入需求文本，生成结构化测试用例并导出。若未配置 API Key，将使用本地规则引擎 fallback。")

default_text = """登录模块需求：
- 支持手机号+密码登录
- 支持手机号+验证码登录（验证码5分钟过期）
- 连续输错密码5次锁定30分钟
- 登录成功生成token，有效期2小时
"""

req = st.text_area("需求描述（可粘贴 Markdown/文本）", value=default_text, height=220)

col1, col2, col3 = st.columns([1,1,2])
with col1:
    out_format = st.selectbox("导出格式", [".xlsx", ".json", ".csv"], index=0)
with col2:
    module_hint = st.text_input("模块提示（可选）", value="")
with col3:
    st.write("")

if module_hint.strip():
    req2 = f"模块：{module_hint.strip()}\n\n" + req
else:
    req2 = req

if st.button("生成测试用例", type="primary"):
    suite = generate_testcases(req2)
    st.success(f"已生成 {len(suite.cases)} 条用例")
    st.subheader("需求摘要")
    st.write(suite.requirement_summary)

    st.subheader("用例列表")
    rows = []
    for c in suite.cases:
        rows.append({
            "id": c.id,
            "module": c.module,
            "title": c.title,
            "priority": c.priority,
            "type": c.type,
            "tags": ",".join(c.tags),
            "preconditions": "\n".join(c.preconditions),
            "steps": "\n".join(c.steps),
            "expected": "\n".join(c.expected),
        })
    st.dataframe(rows, use_container_width=True, height=420)

    with tempfile.TemporaryDirectory() as td:
        out_path = os.path.join(td, "testcases" + out_format)
        export_testcases(suite, out_path)
        with open(out_path, "rb") as f:
            st.download_button(
                label=f"下载 {out_format} 导出文件",
                data=f.read(),
                file_name="testcases" + out_format,
                mime="application/octet-stream"
            )
