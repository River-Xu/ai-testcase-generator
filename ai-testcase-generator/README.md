# AI Testcase Generator (AI 应用岗作品集项目)

一个面向 **AI 应用 / 测试 / 质量保障（QA）** 场景的「测试用例 + 测试数据」自动生成工具：
- 输入：需求描述 / 接口说明 / 业务规则（文本或 Markdown）
- 输出：结构化测试用例（JSON/CSV/XLSX），包含正向/反向/边界/异常/权限/并发等场景
- 支持：任意 **OpenAI-compatible** 大模型（OpenAI / Azure / DeepSeek / 本地兼容网关等）
- 无 API Key 也可运行：提供 **本地规则引擎 fallback**，保证 Demo 可用


---

## 功能特性

- **结构化输出**：统一 TestCase schema（id、模块、标题、前置条件、步骤、期望、优先级、类型、标签）
- **多场景覆盖**：正向 / 反向 / 边界 / 异常 / 安全 / 权限 / 兼容性 / 性能提示
- **一键导出**：JSON / CSV / Excel（XLSX）
- **双入口**：
  - CLI：适合自动化流水线
  - Streamlit Web：适合演示与产品化
- **可插拔模型**：通过环境变量切换模型与 base_url

---

## 快速开始

### 1) 安装依赖（Python 3.10+）

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2) 运行 Web Demo（推荐）

```bash
streamlit run app/streamlit_app.py
```

浏览器打开后，把需求粘贴进去即可生成与导出。

### 3) CLI 用法

```bash
python cli.py --input sample_inputs/requirement_login.md --out outputs/login_cases.xlsx
python cli.py --text "用户注册：手机号+验证码注册，验证码5分钟过期，失败3次锁定10分钟" --out outputs/register_cases.json
```

---

## 配置大模型（可选）

本项目默认**不强制**你配置 API Key；但如果你配置了，将启用 LLM 生成更丰富的用例。

复制一份环境变量文件：

```bash
copy .env.example .env   # Windows
# 或
cp .env.example .env     # macOS/Linux
```

在 `.env` 中填写：

- `OPENAI_API_KEY`：你的 Key
- `OPENAI_MODEL`：默认 `gpt-4o-mini`
- `OPENAI_BASE_URL`：默认 `https://api.openai.com/v1`

> 兼容任意 OpenAI-compatible 网关，例如企业自建网关或其他厂商兼容接口。

---

## 输出数据结构（Schema）

输出字段示例（JSON）：

```json
{
  "id": "TC-001",
  "module": "登录",
  "title": "手机号+密码登录成功",
  "preconditions": ["用户已注册", "账号未锁定"],
  "steps": ["输入正确手机号", "输入正确密码", "点击登录"],
  "expected": ["登录成功", "跳转到首页", "生成有效会话/Token"],
  "priority": "P0",
  "type": "正向",
  "tags": ["功能", "鉴权"]
}
```

---

## 描述

- 设计并实现「AI 测试用例生成器」，基于 Prompt Engineering 生成结构化测试用例并支持一键导出 Excel/JSON；提供 CLI 与 Web Demo，便于团队落地使用  
- 支持 OpenAI-compatible 多模型接入（可切换 base_url/model），并实现无 Key 场景的规则引擎 fallback，保障可演示与可复用  
- 针对需求文本自动覆盖正向/反向/边界/异常/权限等场景，提升测试设计效率与用例一致性

---

---
## Demo 截图 / 使用示例

- Web Demo：通过 Streamlit 提供可视化测试用例生成
<img width="2560" height="1305" alt="image" src="https://github.com/user-attachments/assets/07c399fe-d712-4eee-90e3-cab8d81407fc" />
- CLI Demo：支持命令行批量生成测试用例并导出 Excel
<img width="653" height="118" alt="image" src="https://github.com/user-attachments/assets/fc0b902f-c9c6-45f6-b827-247c2a4b6283" />
---

## 项目结构

```
ai-testcase-generator/
  app/streamlit_app.py
  src/aitestgen/
    generator.py
    prompts.py
    exporters.py
    schemas.py
  sample_inputs/
  outputs/
  cli.py
  requirements.txt
  pyproject.toml
```

---

## License
MIT
