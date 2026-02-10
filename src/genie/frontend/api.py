from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

import sys;
sys.path.append('src');
from genie.cli.build_index import main as build_index
from genie.frontend.routes.chat import router as chat_router
from genie.frontend.routes.batch import router as batch_router
from genie.frontend.routes.eval import router as eval_router

app = FastAPI(title="GENIE")

app.include_router(chat_router, prefix="/api")
app.include_router(batch_router, prefix="/api")
app.include_router(eval_router, prefix="/api")

@app.on_event("startup")
def startup():
    # Control via .env
    if os.getenv("GENIE_BUILD_INDEX", "1") == "1":
        print("🚀 Building index (online)...")
        build_index()
        print("✅ Index ready")

app.mount(
    "/",
    StaticFiles(directory="src/genie/frontend/static", html=True),
    name="static",
)

