from __future__ import print_function
import sys
import time
from redis import Redis, ConnectionError


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def connect_to_redis(host):
    time.sleep(2)
    eprint("Connecting to redis")

    while True:
        try:
            redis = Redis(host=host, db=0)
            redis.ping()
            eprint("Connected to redis")
            return redis
        except ConnectionError:
            eprint("Failed to connect to redis - retrying")
            time.sleep(1)
