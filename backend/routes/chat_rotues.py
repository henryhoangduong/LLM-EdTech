import json
import logging

from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from schemas.schemas import Query

logger = logging.getLogger(__name__)
chat_routes = APIRouter()


@chat_routes.post("/chat")
async def invoke_graph(query: Query = Body(...)):
    pass


@chat_routes.get("/status")
async def health():
    """Check the api is running"""
    return {"status": "🤙"}
