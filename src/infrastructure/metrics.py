from prometheus_client import Counter, Summary, Gauge, Histogram, generate_latest
from fastapi import APIRouter, Request, Response

# Create a router for metrics
metrics_router = APIRouter()

# Define some sample metrics
REQUEST_COUNT = Counter("request_count", "Total number of requests received", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Time taken to process a request in seconds", ["method", "endpoint"])
ERROR_COUNT = Counter("error_count", "Total number of errors", ["method", "endpoint"])

@metrics_router.get("/metrics")
async def metrics_endpoint():
    """Expose Prometheus metrics."""
    return Response(generate_latest(), media_type="text/plain")

@metrics_router.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware to track request metrics."""
    method = request.method
    endpoint = request.url.path
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    with REQUEST_LATENCY.labels(method=method, endpoint=endpoint).time():
        response = await call_next(request)
    return response

def track_error(method: str, endpoint: str):
    """Track error occurrences in the service."""
    ERROR_COUNT.labels(method=method, endpoint=endpoint).inc()
