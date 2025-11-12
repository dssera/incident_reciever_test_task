import asyncio
from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.routes import api, telegram
# from src.models import Base
# from src.config.db_config import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(telegram.set_telegram_webhook())
    yield

app = FastAPI(title="Incident Service", lifespan=lifespan)



@app.get("/")
async def root():
    return RedirectResponse("/docs")


app.include_router(api.router)
app.include_router(telegram.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8011, reload=True)