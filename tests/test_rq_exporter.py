"""RQ's Prometheus exporter tests."""

import requests


def test_job_events(rq_exporter_server, rq_metrics_url):
    """Check metrics events."""
    metrics_response = requests.get(rq_metrics_url.geturl())

    assert metrics_response is not None
    assert 200 == metrics_response.status_code

    assert "rq_request_processing_seconds_count" in metrics_response.text
    assert "rq_request_processing_seconds_sum" in metrics_response.text
    assert "TYPE rq_request_processing_seconds summary" in metrics_response.text

    assert "TYPE rq_workers gauge" in metrics_response.text
    assert "TYPE rq_jobs gauge" in metrics_response.text


def test_job_stats(rq_job_queue, rq_metrics_url):
    """Check job stats correct export."""

    def job1(words):
        """Return size of passed argument."""
        return len(words)

    rq_job_queue.enqueue(job1, "123")
    rq_job_queue.enqueue(job1, "456")

    metrics_response = requests.get(rq_metrics_url.geturl())

    assert metrics_response is not None
    assert 200 == metrics_response.status_code

    assert 'rq_jobs{queue="default",status="queued"} 2.0' in metrics_response.text
    assert 'rq_jobs{queue="default",status="started"} 0.0' in metrics_response.text
    assert 'rq_jobs{queue="default",status="finished"} 0.0' in metrics_response.text
    assert 'rq_jobs{queue="default",status="failed"} 0.0' in metrics_response.text
    assert 'rq_jobs{queue="default",status="deferred"} 0.0' in metrics_response.text
    assert 'rq_jobs{queue="default",status="scheduled"} 0.0' in metrics_response.text


def test_worker_stats(with_worker, rq_metrics_url):
    """Check worker stats correct export."""
    metrics_response = requests.get(rq_metrics_url.geturl())

    assert metrics_response is not None
    assert 200 == metrics_response.status_code

    assert (
        'rq_workers{name="test_worker",queues="default",state="started"} 1.0'
        in metrics_response.text
    )
