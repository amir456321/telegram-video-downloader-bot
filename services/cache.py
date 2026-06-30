import time
import uuid


class Cache:

    def __init__(self):
        self.data = {}

    def create(self, value):

        key = uuid.uuid4().hex

        self.data[key] = {
            "value": value,
            "time": time.time(),
        }

        return key

    def get(self, key):

        item = self.data.get(key)

        if not item:
            return None

        if time.time() - item["time"] > 3600:
            del self.data[key]
            return None

        return item["value"]

    def delete(self, key):
        self.data.pop(key, None)


cache = Cache()
