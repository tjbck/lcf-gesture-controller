from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from ws.main import app as socket_app

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/ws", socket_app, name="socket")


@app.get("/api")
async def get_status():
    return {"status": True}

# wrap with ASGI application
app.mount("/", StaticFiles(directory="./frontend/build", html=True), name="static")
