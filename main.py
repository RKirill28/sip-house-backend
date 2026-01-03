import uvicorn

from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.core.conifg import settings
from src.core.db.helper import create_all
from src.api import main_router

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup app")
    create_all()
    yield
    print("Shutdown app")


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)
