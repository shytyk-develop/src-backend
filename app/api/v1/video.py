from fastapi import APIRouter, HTTPException
import os
from fastapi.responses import FileResponse
from app.schemas.video import (
    VideoAnalyzeRequest,
    VideoAnalyzeResponse,
    VideoDownloadRequest,
    VideoDownloadResponse,
)
from app.services.yt_service import analyze_video, download_video


router = APIRouter(tags=["video"])


# ======================================================
# ANALYZE
# ======================================================

@router.post(
    "/analyze",
    response_model=VideoAnalyzeResponse,
)
def analyze_video_endpoint(payload: VideoAnalyzeRequest):
    try:
        return analyze_video(str(payload.url))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ======================================================
# DOWNLOAD
# ======================================================

@router.post(
    "/download",
)
def download_video_endpoint(payload: VideoDownloadRequest):
    try:
        file_path = download_video(
            video_url=str(payload.url),
            format_id=payload.format_id,
        )
        return FileResponse(file_path, media_type='application/octet-stream', filename=os.path.basename(file_path))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))