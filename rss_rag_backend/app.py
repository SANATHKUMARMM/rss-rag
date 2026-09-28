from fastapi import FastAPI

from rss_rag_backend import scheduler
from rss_rag_backend.route import rag_route

app = FastAPI(lifespan=scheduler.scheduler)

app.include_router(router=rag_route)