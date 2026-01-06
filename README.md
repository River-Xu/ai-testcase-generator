# AI Testcase Generator

An AI-powered application for **automatically generating structured software test cases** from natural language requirements.

This project is designed for **QA / AI application roles**, focusing on practical AI-assisted testing workflows rather than theoretical model training.

---

## Why this project

In real software projects, test case design is:
- Time-consuming
- Highly repetitive
- Strongly dependent on individual experience

This project explores how large language models (LLMs) can assist QA engineers by:
- Converting unstructured requirements into structured test cases
- Improving coverage consistency
- Reducing manual effort in early test design stages

---

## What it does

- Accepts requirement descriptions in natural language
- Generates structured test cases with:
  - Test ID
  - Module
  - Title
  - Preconditions
  - Steps
  - Expected Results
  - Priority
  - Tags
- Supports multiple output formats:
  - Excel (`.xlsx`)
  - JSON
  - CSV
- Provides both:
  - **Web UI (Streamlit)**
  - **Command-line interface (CLI)**
- Works **without API key** using rule-based + prompt fallback logic

---

## Typical Use Cases

- QA engineers drafting test cases from PRD / requirement docs
- AI-assisted test design in early development stages
- Test case standardization across teams
- Demonstrating AI application capability in QA workflows

---

## Architecture Overview

