import logging
import os
from contextlib import asynccontextmanager

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import Settings
from core.utils.logger import setup_logging
from routes import auth_routes, course_routes, role_routes

dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)

load_dotenv()
setup_logging(level=logging.INFO)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_routes, prefix="/api/auth", tags=["Auth"])
app.include_router(role_routes, prefix="/api/role", tags=["Roles"])
app.include_router(
    course_routes, prefix="/api/course", tags=["Courses"])


settings = Settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
