import os
import ssl

import dotenv
import uvicorn
from fastapi import FastAPI

from rss_rag_backend import scheduler
from rss_rag_backend.route import rag_route

dotenv.load_dotenv(override=True)

app = FastAPI(lifespan=scheduler.scheduler)

app.include_router(router=rag_route)

if __name__ == '__main__':
    port = int(os.environ.get("PORT",9191))
    uvicorn.run(app, host="127.0.0.1", port=port)