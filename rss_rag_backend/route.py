from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Form
from fastapi.sse import EventSourceResponse
from starlette.responses import StreamingResponse

from rss_agent import invoke

rag_route = APIRouter(prefix="/agent", tags=["agent"])

@rag_route.post("/query")
def query_rag_agent(query: Annotated[str, Form(max_length=200)]):
    return StreamingResponse(content=invoke.invoke_agent(query),media_type="text/event-stream")