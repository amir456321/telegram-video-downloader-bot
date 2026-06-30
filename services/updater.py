import subprocess
import threading
import time


class Updater:

    def run(self):

        while True:

            try:

                subprocess.run(
                    ["pip", "install", "-U", "yt-dlp"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

            except Exception:
                pass

            # هر 24 ساعت
            time.sleep(60 * 60 * 24)


def start_updater():

    thread = threading.Thread(
        target=Updater().run,
        daemon=True,
    )

    thread.start()
