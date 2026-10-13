"""模型部署记录的请求与响应数据结构。"""

from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class ModelCreate(BaseModel):
    """登记模型部署记录时使用的输入结构。"""

    name: str = Field(min_length=1, max_length=120)
    provider: Literal["local", "vllm", "openai-compatible", "other"] = "local"
    endpoint: str | None = Field(default=None, max_length=2048)
    description: str | None = Field(default=None, max_length=1000)


class ModelRecord(BaseModel):
    """API 返回的模型元数据。"""

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)
    name: str
    provider: str
    endpoint: str | None = None
    description: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
