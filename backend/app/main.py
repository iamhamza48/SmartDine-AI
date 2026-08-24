from fastapi import FastAPI
from app.api.routes import inventory
from app.api.routes import chat
from app.api.routes import approvals
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Restaurant AI Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(inventory.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(approvals.router, prefix="/api")






@app.get("/health")
def health():
    return {"status": "ok"}