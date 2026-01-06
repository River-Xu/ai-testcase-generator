from __future__ import annotations
from typing import List, Literal
from pydantic import BaseModel, Field

Priority = Literal["P0", "P1", "P2", "P3"]
CaseType = Literal["正向", "反向", "边界", "异常", "权限", "安全", "性能", "兼容性", "其他"]

class TestCase(BaseModel):
    id: str = Field(..., description="Test case id, e.g., TC-001")
    module: str = Field(..., description="Functional module, e.g., 登录")
    title: str = Field(..., description="Short case title")
    preconditions: List[str] = Field(default_factory=list)
    steps: List[str] = Field(default_factory=list)
    expected: List[str] = Field(default_factory=list)
    priority: Priority = "P1"
    type: CaseType = "正向"
    tags: List[str] = Field(default_factory=list)

class TestCaseSuite(BaseModel):
    requirement_summary: str
    cases: List[TestCase]
