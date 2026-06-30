import os
import uuid
import yt_dlp

from config import DOWNLOAD_DIR


class Downloader:

    def download(self, url: str, format_id: str):

        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        output = os.path.join(
            DOWNLOAD_DIR,
            f"{uuid.uuid4()}.%(ext)s"
        )

        ydl_opts = {
            "format": f"{format_id}+bestaudio/best",
            "outtmpl": output,
            "merge_output_format": "mp4",
            "noplaylist": True,
            "quiet": True,
            "retries": 10,
            "fragment_retries": 10,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            return ydl.prepare_filename(info)
