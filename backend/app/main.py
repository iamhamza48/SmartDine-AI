from fastapi import FastAPI
from app.api.routes import inventory
from app.api.routes import chat
from app.api.routes import approvals
from app.api.routes import runs
from app.config.settings import settings
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Restaurant AI Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin
        for origin in [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            settings.frontend_url,
        ]
        if origin
    ],
    allow_origin_regex=r"https://[a-z0-9-]+\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(inventory.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(approvals.router, prefix="/api")
app.include_router(runs.router, prefix="/api")






@app.get("/health")
def health():
    return {"status": "ok"}