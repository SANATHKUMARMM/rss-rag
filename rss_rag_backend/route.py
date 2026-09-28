from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Form
from fastapi.sse import EventSourceResponse

from rss_agent import invoke

rag_route = APIRouter(prefix="/agent", tags=["agent"])

@rag_route.post("query",response_class=EventSourceResponse)
async def query_rag_agent(query: Annotated[str, Form(max_length=200)]):
    return invoke.invoke_agent(query)