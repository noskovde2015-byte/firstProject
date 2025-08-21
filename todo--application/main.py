from fastapi import FastAPI, middleware, Request
import uvicorn
from api import router as api_router
from core.config import settings
from core.middlewares.middlewares import aut_middleware


app = FastAPI()
app.include_router(api_router)

app.middleware("http")(aut_middleware)



if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)