"""Configuration file for exporting."""

import os

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = "8765"
DEFAULT_REDIS_HOST = "localhost"
DEFAULT_REDIS_PORT = "6379"
DEFAULT_REDIS_DB = "0"
DEFAULT_REDIS_PASS = None
DEFAULT_REDIS_IS_SENTINEL = "false"
DEFAULT_REDIS_MASTER_SET = "mymaster"
DEFAULT_LOG_LEVEL = "INFO"

DEFAULT_LOG_FORMAT = "[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s"
DEFAULT_LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"

HOST = os.environ.get("RQ_EXPORTER_HOST", DEFAULT_HOST)
PORT = os.environ.get("RQ_EXPORTER_PORT", DEFAULT_PORT)

REDIS_HOST = os.environ.get("RQ_REDIS_HOST", DEFAULT_REDIS_HOST)
REDIS_PORT = int(os.environ.get("RQ_REDIS_PORT", DEFAULT_REDIS_PORT))
REDIS_DB = int(os.environ.get("RQ_REDIS_DB", DEFAULT_REDIS_DB))
REDIS_PASS = os.environ.get("RQ_REDIS_PASS", DEFAULT_REDIS_PASS)
REDIS_IS_SENTINEL = (
    os.environ.get("RQ_REDIS_IS_SENTINEL", DEFAULT_REDIS_IS_SENTINEL) == "true"
)
REDIS_MASTER_SET = os.environ.get("RQ_REDIS_MASTER_SET", DEFAULT_REDIS_MASTER_SET)

if REDIS_IS_SENTINEL:
    from redis.sentinel import Sentinel

    sentinel = Sentinel(
        [(REDIS_HOST, REDIS_PORT)],
        sentinel_kwargs={"password": REDIS_PASS},
    )
    REDIS_HOST, REDIS_PORT = sentinel.discover_master(REDIS_MASTER_SET)

LOG_LEVEL = os.environ.get("RQ_EXPORTER_LOG_LEVEL", DEFAULT_LOG_LEVEL).upper()
LOG_FORMAT = os.environ.get("RQ_EXPORTER_LOG_FORMAT", DEFAULT_LOG_FORMAT)
LOG_DATEFMT = os.environ.get("RQ_EXPORTER_LOG_DATEFMT", DEFAULT_LOG_DATEFMT)
