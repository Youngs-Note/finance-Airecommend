from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.app.api import health, products, recommendations, stats
from backend.app.core.config import get_settings
from backend.app.core.errors import (
    ApplicationError,
    ConfigurationError,
    ExternalApiError,
    ProductNotFoundError,
)

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.include_router(health.router)
app.include_router(products.router)
app.include_router(recommendations.router)
app.include_router(stats.router)


@app.exception_handler(ApplicationError)
async def handle_application_error(_request: Request, error: ApplicationError) -> JSONResponse:
    status_code = 400
    if isinstance(error, ProductNotFoundError):
        status_code = 404
    elif isinstance(error, ExternalApiError):
        status_code = 502
    elif isinstance(error, ConfigurationError):
        status_code = 503
    return JSONResponse(status_code=status_code, content={"detail": str(error)})


@app.get("/", include_in_schema=False)
async def index() -> dict[str, str]:
    return {
        "service": settings.app_name,
        "status": "ok",
        "docs": "/docs",
    }
