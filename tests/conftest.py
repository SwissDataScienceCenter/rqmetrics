import os
import time

import pytest
from rq import Worker

from rqmetrics.exporter import RQPrometheusExporter
from rqmetrics.config import REDIS_DB, REDIS_HOST, REDIS_PASS, REDIS_PORT

from redis import Redis


def get_test_cache():
    """Return cache connection for testing."""
    cache = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASS)
    return cache


@pytest.fixture(scope="module")
def rq_exporter_addr():
    """Return interface and port for RQ exporter."""
    host = os.getenv("RQ_HOST_ADDRESS", "0.0.0.0")
    port = int(os.getenv("RQ_HOST_PORT", "8087"))
    return port, host


@pytest.fixture(scope="module")
def rq_metrics_url(rq_exporter_addr):
    """Return URL where metrics are hosted."""
    from urllib.parse import urlparse

    port, addr = rq_exporter_addr
    return urlparse(f"http://{addr}:{port}")


@pytest.fixture(scope="module")
def rq_exporter_server(rq_exporter_addr):
    """RQ's Prometheus exporter."""
    from prometheus_client import start_wsgi_server
    from prometheus_client.core import REGISTRY

    REGISTRY.register(RQPrometheusExporter(get_test_cache(), ""))
    start_wsgi_server(*rq_exporter_addr)

    yield


@pytest.fixture
def rq_job_queue(rq_exporter_server):
    """RQ's job queue."""
    from rq import Queue

    yield Queue(connection=get_test_cache())


@pytest.fixture
def with_worker(rq_exporter_server):
    """Start worker."""
    from threading import Event, Thread

    ready = Event()

    def make_worker():
        """Create and start a worker."""
        worker = Worker(["default"], name="test_worker", connection=get_test_cache())
        ready.set()
        worker.work()

    Thread(target=make_worker).start()
    time.sleep(2)

    yield
