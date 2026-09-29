"""
Scheduler for adding RSS Feed in equal intervals
"""
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from rss_agent.embedding import add_rss_document


@asynccontextmanager
async def scheduler(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(add_rss_document, 'interval',args=["http://127.0.0.1:8181/feed/"], minutes=1)
    scheduler.start()
    yield
    scheduler.shutdown()
