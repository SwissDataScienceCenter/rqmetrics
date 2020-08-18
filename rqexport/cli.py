"""CLI interface for RQ exporter."""

import signal
import sys
import time

from prometheus_client import start_wsgi_server
from prometheus_client.core import REGISTRY
from redis import Redis, RedisError

from rqexport.config import HOST, PORT, REDIS_DB, REDIS_HOST, REDIS_PASS, REDIS_PORT
from rqexport.exporter import RQPrometheusExporter
from rqexport.logger import logger


def sig_handle(sig, frame):
    """Handle OS signals."""
    logger.info("Stopping the server")
    sys.exit(0)


def bootstrap_metrics_server():
    """Configure and bootstrap metrics server."""
    try:
        logger.info("Creating cache connection")
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
