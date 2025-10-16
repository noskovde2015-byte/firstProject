from fastapi import FastAPI, middleware, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router
from core.config import settings
from core.middlewares.middlewares import aut_middleware



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)

app.middleware("http")(aut_middleware)

@app.get("/")
async def root():
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)