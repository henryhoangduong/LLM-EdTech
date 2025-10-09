import json
import logging

from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from schemas.schemas import Query
from services.chatbots.chat4u.graph import graph
from services.chatbots.chat4u.state import State, for_client

logger = logging.getLogger(__name__)
chat_routes = APIRouter()


@chat_routes.post("/chat")
async def invoke_graph(query: Query = Body(...)):
    config = {"configurable": {"thread_id": "2"}}
    state = State()
    state["messages"] = [HumanMessage(content=query.message)]

    def is_numeric(s):
        import re

        return bool(re.match(r"^[\d ]+$", s.strip()))

    async def generate_response():
        try:
            buffer = ""
            last_state = None
            async for event in graph.astream_events(state, version="v2", config=config):
                event.get("metadata", {})
                event_type = event.get("event")

                if event_type == "on_chain_end" and event["name"] == "retrieve":
                    state["documents"] = event["data"]["output"]["documents"]
                    last_state = for_client(state)
                    yield f"{json.dumps({'state': last_state})}\n\n"
                if event_type == "on_chat_model_stream":
                    chunk = event["data"]["chunk"].content
                    state_snapshot = for_client(state)
                    last_state = state_snapshot
                    if is_numeric(chunk) or (buffer and chunk in [" ", ",", "."]):
                        buffer += chunk
                    else:
                        if buffer:
                            combined = buffer + chunk
                            yield f"{json.dumps({'content': combined, 'state': last_state})}\n\n"
                            buffer = ""
                        else:
                            yield f"{json.dumps({'content': chunk, 'state': last_state})}\n\n"
                elif event_type == "on_chat_end":
                    # Send the latest state that now includes documents
                    yield f"{json.dumps({'state': last_state})}\n\n"
        except Exception as e:
            logger.error("Error invoking graph: ", e)
            yield f"{json.dumps({'error': str(e)})}\n\n"
        finally:
            print("Done")


@chat_routes.get("/status")
async def health():
    """Check the api is running"""
    return {"status": "🤙"}
