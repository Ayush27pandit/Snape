from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import redis.asyncio as redis
from sqlalchemy import text

from src.core.config import settings
from src.db.session import init_db, close_db, engine
from src.api.routes import analyze, brands, memory, comparisons
from src.workers.analysis_worker import get_worker, start_worker


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    worker = await get_worker()
    # Start worker in background
    import asyncio
    asyncio.create_task(start_worker())
    yield
    # Shutdown
    await close_db()
    await worker.close()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Snape - Competitive Intelligence API",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(analyze.router, prefix=settings.API_PREFIX)
app.include_router(brands.router, prefix=settings.API_PREFIX)
app.include_router(memory.router, prefix=settings.API_PREFIX)
app.include_router(comparisons.router, prefix=settings.API_PREFIX)


@app.get("/health")
async def health_check():
    """Basic health check - no dependencies."""
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.get("/health/ready")
async def readiness_check():
    """Readiness check - verifies all dependencies are available."""
    checks = {}
    overall_healthy = True

    # Check database
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        checks["database"] = {"status": "healthy", "details": "Connected"}
    except Exception as e:
        checks["database"] = {"status": "unhealthy", "details": str(e)}
        overall_healthy = False

    # Check Redis
    try:
        r = redis.from_url(settings.REDIS_URL, decode_responses=True)
        await r.ping()
        await r.close()
        checks["redis"] = {"status": "healthy", "details": "Connected"}
    except Exception as e:
        checks["redis"] = {"status": "unhealthy", "details": str(e)}
        overall_healthy = False

    status_code = 200 if overall_healthy else 503
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "ready" if overall_healthy else "not_ready",
            "version": settings.APP_VERSION,
            "checks": checks,
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc) if settings.DEBUG else None},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )