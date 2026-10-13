"""Request and response schemas for model deployment records."""

from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class ModelCreate(BaseModel):
    """Input used to register a model deployment record."""

    name: str = Field(min_length=1, max_length=120)
    provider: Literal["local", "vllm", "openai-compatible", "other"] = "local"
    endpoint: str | None = Field(default=None, max_length=2048)
    description: str | None = Field(default=None, max_length=1000)


class ModelRecord(BaseModel):
    """Model metadata returned by the API."""

    model_config = ConfigDict(frozen=True)

    id: UUID = Field(default_factory=uuid4)
    name: str
    provider: str
    endpoint: str | None = None
    description: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
