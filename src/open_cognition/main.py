from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from surreal_basics.migrate import AsyncMigrationRunner

from open_cognition.config import OC_HOST, OC_PORT, ensure_data_dir, get_migrations_dir


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_data_dir()
    migrations_dir = get_migrations_dir()
    logger.info(f"Using migrations from: {migrations_dir}")
    runner = AsyncMigrationRunner(migrations_dir)
    applied = await runner.run_up()
    for m in applied:
        logger.info(f"Applied migration {m.version:03d}_{m.name}")
    yield


app = FastAPI(title="open-cognition", version="0.1.0", lifespan=lifespan)

from open_cognition.frontend.routes import router as frontend_router  # noqa: E402
from open_cognition.routes.artifact_routes import router as artifact_router  # noqa: E402
from open_cognition.routes.doubt_routes import router as doubt_router  # noqa: E402
from open_cognition.routes.flashcard_routes import router as flashcard_router  # noqa: E402
from open_cognition.routes.resource_routes import router as resource_router  # noqa: E402
from open_cognition.routes.topic_routes import router as topic_router  # noqa: E402

app.include_router(topic_router, prefix="/api")
app.include_router(flashcard_router, prefix="/api")
app.include_router(resource_router, prefix="/api")
app.include_router(artifact_router, prefix="/api")
app.include_router(doubt_router, prefix="/api")
app.include_router(frontend_router)


@app.get("/health")
async def health():
    return {"status": "ok"}


def run():
    import uvicorn

    uvicorn.run("open_cognition.main:app", host=OC_HOST, port=OC_PORT, reload=True)
