"""用于学习 API 工程化与服务运维的 FastAPI 示例。"""

from collections.abc import Sequence
from uuid import UUID

from fastapi import FastAPI, HTTPException, status

from model_ops_api.schemas import ModelCreate, ModelRecord

app = FastAPI(
    title="LLMOps 实验室模型运维 API",
    version="0.1.0",
    description="用于登记模型部署元数据的学习型 API。",
)

# 第一阶段刻意使用内存存储，方便理解接口设计；这不是持久化存储。
_models: dict[UUID, ModelRecord] = {}


@app.get("/health", tags=["运维"])
def health() -> dict[str, str]:
    """返回基础存活状态。"""
    return {"status": "ok"}


@app.post(
    "/api/v1/models",
    response_model=ModelRecord,
    status_code=status.HTTP_201_CREATED,
    tags=["模型"],
)
def create_model(payload: ModelCreate) -> ModelRecord:
    """登记一条模型部署记录。"""
    record = ModelRecord(**payload.model_dump())
    _models[record.id] = record
    return record


@app.get("/api/v1/models", response_model=list[ModelRecord], tags=["模型"])
def list_models() -> Sequence[ModelRecord]:
    """列出所有模型记录，顺序与登记顺序一致。"""
    return list(_models.values())


@app.get("/api/v1/models/{model_id}", response_model=ModelRecord, tags=["模型"])
def get_model(model_id: UUID) -> ModelRecord:
    """按 ID 查询一条模型记录。"""
    record = _models.get(model_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到该模型")
    return record
