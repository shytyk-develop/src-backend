from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.api.v1.video import router as video_router


# ======================================================
# APP
# ======================================================

app = FastAPI(
    title="YT Downloader API",
    version="1.0.0",
)


# ======================================================
# CORS
# ======================================================
# ВАЖНО:
# - allow_credentials = False (fetch + разные домены)
# - "*" нельзя использовать с credentials
# - методы ограничиваем

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все origins для разработки
    allow_methods=["GET", "POST", "OPTIONS"],  # Ограничить методы
    allow_headers=["*"],
    allow_credentials=False,
)


# ======================================================
# STATIC FILES
# ======================================================

# Убрано для serverless, файлы возвращаются напрямую


# ======================================================
# ROOT
# ======================================================

@app.get("/")
def root():
    return {"message": "YouTube Downloader API is running"}


# ======================================================
# ROUTERS
# ======================================================

app.include_router(video_router, prefix="/video")