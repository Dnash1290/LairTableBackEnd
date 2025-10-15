from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3, uvicorn, sys
from Handler.handler import conn_router

sys.dont_write_bytecode = True
app = FastAPI()

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    conn_router,
    prefix="/conn_router",
    tags=["User Connetion Router"]
)

@app.get("/")
def read_root():
    return {"message": "lowtaperfaaade"*4}

@app.get("/api/test")
def test_endpoint():
    return {"data": "This is test data from backend"}

