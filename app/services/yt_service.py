import yt_dlp
import os
import time
from typing import Dict, List


# ======================================================
# КОНФИГ ПУТЕЙ
# ======================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS_FOLDER = "/tmp/downloads"  # Использовать /tmp для Vercel serverless

os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)


# ======================================================
# АНАЛИЗ ВИДЕО
# ======================================================

def analyze_video(video_url: str) -> Dict:
    if not video_url:
        raise ValueError("video_url is required")

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        video_data = ydl.extract_info(video_url, download=False)

    duration = video_data.get("duration", 0)
    duration_minutes = duration // 60
    duration_seconds = duration % 60

    formats = video_data.get("formats", [])

    filtered_formats: List[Dict] = []
    seen_qualities = set()

    for fmt in formats:
        height = fmt.get("height")
        ext = fmt.get("ext")
        format_id = fmt.get("format_id")

        vcodec = fmt.get("vcodec")
        acodec = fmt.get("acodec")

        has_video = vcodec != "none"
        has_audio = acodec != "none"

        if not has_video:
            continue

        if not height:
            continue

        if ext == "mhtml":
            continue

        if height >= 1440:
            if ext not in ("mp4", "webm"):
                continue
        else:
            if ext != "mp4":
                continue

        quality_key = f"{height}_{ext}"
        if quality_key in seen_qualities:
            continue

        seen_qualities.add(quality_key)

        filtered_formats.append({
            "label": f"{height}p",
            "height": height,
            "format_id": format_id,
            "file_extension": ext,
            "contains_audio": has_audio,
            "file_size": fmt.get("filesize") or 0,
        })

    filtered_formats.sort(key=lambda x: x["height"], reverse=True)

    if filtered_formats:
        max_height = filtered_formats[0]["height"]
        recommended_format = f"bestvideo[height<={max_height}]+bestaudio/best"
    else:
        recommended_format = "best"

    return {
        "video": {
            "title": video_data.get("title"),
            "author": video_data.get("uploader"),
            "duration": f"{duration_minutes}:{duration_seconds:02d}",
            "thumbnail": video_data.get("thumbnail"),
            "url": video_url,
        },
        "available_formats": filtered_formats,
        "recommended_format": recommended_format,
    }


# ======================================================
# СКАЧИВАНИЕ ВИДЕО
# ======================================================

def download_video(video_url: str, format_id: str) -> str:
    if not video_url:
        raise ValueError("video_url is required")

    if not format_id:
        raise ValueError("format_id is required")

    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        video_data = ydl.extract_info(video_url, download=False)

    final_format = format_id

    output_template = os.path.join(
        DOWNLOADS_FOLDER,
        f"video_{int(time.time())}_%(title)s.%(ext)s"
    )

    def progress_hook(d):
        if d["status"] == "finished":
            pass  # намеренно пусто (serverless-safe)

    ydl_opts = {
        "format": final_format,
        "outtmpl": output_template,
        "progress_hooks": [progress_hook],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        file_path = ydl.prepare_filename(info)

    if not os.path.exists(file_path):
        raise FileNotFoundError("Downloaded file not found")

    return file_path