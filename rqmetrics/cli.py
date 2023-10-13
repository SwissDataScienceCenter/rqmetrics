"""CLI interface for RQ exporter."""

import signal
import sys
import time

from prometheus_client import start_wsgi_server
from prometheus_client.core import REGISTRY
from redis import Redis, RedisError, Sentinel

from rqmetrics.config import HOST, PORT, REDIS_DB, REDIS_HOST, REDIS_PASS, REDIS_PORT, REDIS_IS_SENTINEL, REDIS_MASTER_SET
from rqmetrics.exporter import RQPrometheusExporter
from rqmetrics.logger import logger


def sig_handle(sig, frame):
    """Handle OS signals."""
    logger.info("Stopping the server")
    sys.exit(0)


def bootstrap_metrics_server():
    """Configure and bootstrap metrics server."""
    logger.info("Creating cache connection")
    
    try:
        if REDIS_IS_SENTINEL:
            sentinel = Sentinel([(REDIS_HOST, REDIS_PORT)], sentinel_kwargs={"password": REDIS_PASS})
            cache = sentinel.master_for(REDIS_MASTER_SET, db=REDIS_DB, password=REDIS_PASS, retry_on_timeout=True, health_check_interval=30)
        else:
            cache = Redis(
                host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASS
            )

        logger.info("Registering RQ Prometheus exporter")
        REGISTRY.register(RQPrometheusExporter(cache))
    except (RedisError, IOError) as exp:
        logger.exception(exp)
        sys.exit(1)

    logger.info("Starting a metrics server")
    start_wsgi_server(int(PORT), HOST)

    signal.signal(signal.SIGINT, sig_handle)
    signal.signal(signal.SIGTERM, sig_handle)


def main():
    """Entry point for RQ exporter."""
    bootstrap_metrics_server()

    while True:
        time.sleep(1)
