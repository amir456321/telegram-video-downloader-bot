import yt_dlp


class YTDLP:

    def _opts(self):
        return {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "noplaylist": True,
        }

    def info(self, url):
        with yt_dlp.YoutubeDL(self._opts()) as ydl:
            return ydl.extract_info(url, download=False)

    def formats(self, url):

        info = self.info(url)

        qualities = {}

        for f in info.get("formats", []):

            if f.get("vcodec") == "none":
                continue

            h = f.get("height")

            if not h:
                continue

            old = qualities.get(h)

            if old is None or f.get("tbr", 0) > old.get("tbr", 0):

                qualities[h] = {
                    "id": f["format_id"],
                    "height": h,
                    "tbr": f.get("tbr", 0)
                }

        return sorted(
            qualities.values(),
            key=lambda x: x["height"]
        )
