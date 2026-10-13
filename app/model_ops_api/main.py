"""用于学习 API 工程化与服务运维的 FastAPI 示例。"""

from collections.abc import Awaitable, Callable, Sequence
from time import perf_counter
from uuid import UUID

from fastapi import FastAPI, HTTPException, Request, Response, status
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from model_ops_api.schemas import ModelCreate, ModelRecord

app = FastAPI(
    title="LLMOps 实验室模型运维 API",
    version="0.1.0",
    description="用于登记模型部署元数据的学习型 API。",
)

# 第一阶段刻意使用内存存储，方便理解接口设计；这不是持久化存储。
_models: dict[UUID, ModelRecord] = {}

HTTP_REQUESTS = Counter(
    "llmops_http_requests_total",
    "HTTP requests handled by the API, excluding the metrics endpoint.",
    ("method", "route", "status"),
)
HTTP_REQUEST_DURATION = Histogram(
    "llmops_http_request_duration_seconds",
    "HTTP request duration in seconds, excluding the metrics endpoint.",
    ("method", "route"),
)


@app.middleware("http")
async def observe_http_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """记录低基数 HTTP 指标；绝不使用原始 URL、用户 ID 或提示词作为标签。"""
    if request.url.path == "/metrics":
        return await call_next(request)

    started = perf_counter()
    response = await call_next(request)
    duration = perf_counter() - started
    route_object = request.scope.get("route")
    route = getattr(route_object, "path", "unmatched")
    HTTP_REQUESTS.labels(request.method, route, str(response.status_code)).inc()
    HTTP_REQUEST_DURATION.labels(request.method, route).observe(duration)
    return response


@app.get("/metrics", include_in_schema=False, tags=["运维"])
def metrics() -> Response:
    """以 Prometheus exposition 格式导出应用指标。"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/health", tags=["运维"])
def health() -> dict[str, str]:
    """返回基础存活状态；它不代表外部模型推理已经可用。"""
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
