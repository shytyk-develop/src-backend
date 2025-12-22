from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional


# ======================================================
# ANALYZE
# ======================================================

class VideoAnalyzeRequest(BaseModel):
    url: HttpUrl = Field(..., description="YouTube video URL")


class AvailableFormat(BaseModel):
    label: str
    height: int
    format_id: str
    file_extension: str
    contains_audio: bool
    file_size: int


class VideoInfo(BaseModel):
    title: Optional[str]
    author: Optional[str]
    duration: str
    thumbnail: Optional[HttpUrl]
    url: HttpUrl


class VideoAnalyzeResponse(BaseModel):
    video: VideoInfo
    available_formats: List[AvailableFormat]
    recommended_format: str


# ======================================================
# DOWNLOAD
# ======================================================

class VideoDownloadRequest(BaseModel):
    url: HttpUrl = Field(..., description="YouTube video URL")
    format_id: str = Field(..., description="yt-dlp format_id")


class VideoDownloadResponse(BaseModel):
    download_url: str