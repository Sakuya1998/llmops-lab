"""Small FastAPI service for learning API engineering and operations."""

from collections.abc import Sequence
from uuid import UUID

from fastapi import FastAPI, HTTPException, status

from model_ops_api.schemas import ModelCreate, ModelRecord

app = FastAPI(
    title="LLMOps Lab Model Operations API",
    version="0.1.0",
    description="A learning API for registering model deployment metadata.",
)

# Deliberately in-memory for the first learning milestone. This is not durable storage.
_models: dict[UUID, ModelRecord] = {}


@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    """Return a basic liveness response."""
    return {"status": "ok"}


@app.post(
    "/api/v1/models",
    response_model=ModelRecord,
    status_code=status.HTTP_201_CREATED,
    tags=["models"],
)
def create_model(payload: ModelCreate) -> ModelRecord:
    """Register a model deployment record."""
    record = ModelRecord(**payload.model_dump())
    _models[record.id] = record
    return record


@app.get("/api/v1/models", response_model=list[ModelRecord], tags=["models"])
def list_models() -> Sequence[ModelRecord]:
    """List model records in insertion order."""
    return list(_models.values())


@app.get("/api/v1/models/{model_id}", response_model=ModelRecord, tags=["models"])
def get_model(model_id: UUID) -> ModelRecord:
    """Fetch one model record by ID."""
    record = _models.get(model_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Model not found")
    return record
