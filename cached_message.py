import hashlib
import json

import redis
from cachetools import cached


@cached({})
def get_redis() -> redis.Redis:
    return redis.Redis("redis")


class CachedMessage(dict):

    def __init__(self, *args, _id=None, _key=None, _bus=get_redis(), **kwargs):
        super().__init__(*args, **kwargs)
        self._bus = _bus
        self._id = _id
        self._key = _key
        self._checksum = None

    @property
    def redis_checksum_key(self):
        return f"{self._key}_checksum:{self._id}"

    @property
    def checksum(self):
        if self._checksum is None:
            self._checksum = hashlib.md5(
                json.dumps(self, sort_keys=True).encode()
            ).hexdigest()
        return self._checksum

    @property
    def checksum_in_cache(self):
        checksum = self._bus.get(self.redis_checksum_key)
        if checksum is not None:
            return checksum.decode()

    @property
    def is_checksum_valid(self):
        return self.checksum == self.checksum_in_cache

    def checksum_to_cash(self):
        return self._bus.set(self.redis_checksum_key, self.checksum)

