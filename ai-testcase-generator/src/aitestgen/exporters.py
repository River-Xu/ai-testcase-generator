from __future__ import annotations
import json
import os
from typing import Union
import pandas as pd
from .schemas import TestCaseSuite

def _suite_to_rows(suite: TestCaseSuite):
    rows = []
    for c in suite.cases:
        rows.append({
            "id": c.id,
            "module": c.module,
            "title": c.title,
            "preconditions": "\n".join(c.preconditions),
            "steps": "\n".join(c.steps),
            "expected": "\n".join(c.expected),
            "priority": c.priority,
            "type": c.type,
            "tags": ",".join(c.tags),
        })
    return rows

def export_testcases(suite: TestCaseSuite, out_path: str) -> str:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    ext = os.path.splitext(out_path)[1].lower()

    if ext in [".json"]:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(suite.model_dump(), f, ensure_ascii=False, indent=2)
        return out_path

    rows = _suite_to_rows(suite)
    df = pd.DataFrame(rows)

    if ext in [".csv"]:
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        return out_path

    if ext in [".xlsx"]:
        with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="testcases")
            # Add a second sheet with summary for readability
            summary_df = pd.DataFrame([{"requirement_summary": suite.requirement_summary}])
            summary_df.to_excel(writer, index=False, sheet_name="summary")
        return out_path

    raise ValueError(f"Unsupported output format: {ext}. Use .json/.csv/.xlsx")
