from routes.auth_routes import auth_routes
from routes.chat_rotues import chat_routes
from routes.course_routes import course_routes
from routes.embedding_routes import embedding_routes
from routes.ingestion_routes import ingestion_routes
from routes.role_routes import role_routes

__all__ = ["auth_routes", "course_routes",
           "role_routes", "ingestion_routes", "chat_routes", "embedding_routes"]
