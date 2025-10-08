import logging
from contextlib import asynccontextmanager

from core.config import settings
from core.utils.logger import setup_logging
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import (auth_routes, chat_routes, course_routes, embedding_routes,
                    ingestion_routes, role_routes)

dotenv_path = find_dotenv()
print("dotenv path: ", dotenv_path)
if dotenv_path:
    load_dotenv(dotenv_path)

load_dotenv()
setup_logging(level=logging.INFO)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 50)
    logger.info("Starting BDA Application")
    logger.info("=" * 50)

    # Frontend Config
    logger.info('Frontend Origin: ' + settings.frontend.frontend_origin)
    logger.info("=" * 50)

    # Database Config
    logger.info('Database Provider: ' + settings.database.provider)
    logger.info("=" * 50)

    # Postgres Config
    logger.info('Postgres User: ' + settings.postgres.user)
    logger.info('Postgres Password: ' + settings.postgres.password)
    logger.info('Postgres Host: ' + settings.postgres.host)
    logger.info('Postgres Port: ' + settings.postgres.port)
    logger.info("=" * 50)

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_routes, prefix="/api/auth", tags=["Auth"])
app.include_router(role_routes, prefix="/api/role", tags=["Roles"])
app.include_router(
    ingestion_routes, prefix="/api/ingestion", tags=["Ingestion"])
app.include_router(
    course_routes, prefix="/api/course", tags=["Courses"])
app.include_router(chat_routes, prefix="/api/chat", tags=["Chat"])
app.include_router(
    embedding_routes, prefix="/api/embedding", tags=["Embedding"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
