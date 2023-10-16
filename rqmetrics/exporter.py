"""Export RQ metrics."""
from prometheus_client import Summary
from prometheus_client.core import GaugeMetricFamily
from rq import Connection, Queue, Worker
from rq.job import JobStatus


class RQPrometheusExporter:
    """RQ's metrics exporter for Prometheus."""

    summary = Summary("rq_request_processing_seconds", "Collect time metric")

    def __init__(self, cache, namespace):
        """Construct exporter."""
        self.cache = cache
        self.namespace = namespace

    def worker_metrics(self):
        """Get RQ worker metrics."""
        rq_workers_gauge = GaugeMetricFamily(
            "rq_workers", "RQ workers", labels=["name", "state", "queues"]
        )

        for worker in Worker.all():
            rq_workers_gauge.add_metric(
                [worker.name, worker.get_state(), ",".join(worker.queue_names())], 1
            )

        return rq_workers_gauge

    def queue_metrics(self):
        """Get RQ queue metrics."""
        rq_jobs_gauge = GaugeMetricFamily(
            "rq_jobs", "RQ jobs by state", labels=["queue", "status"]
        )

        for q in Queue.all():
            if not q.name.startswith(self.namespace):
                # Only track metrics for queues associated with the current core-svc
                continue

            rq_jobs_gauge.add_metric([q.name, JobStatus.QUEUED], q.count)
            rq_jobs_gauge.add_metric(
                [q.name, JobStatus.STARTED], q.started_job_registry.count
            )
            rq_jobs_gauge.add_metric(
                [q.name, JobStatus.FINISHED], q.finished_job_registry.count
            )
            rq_jobs_gauge.add_metric(
                [q.name, JobStatus.FAILED], q.failed_job_registry.count
            )
            rq_jobs_gauge.add_metric(
                [q.name, JobStatus.DEFERRED], q.deferred_job_registry.count
            )
            rq_jobs_gauge.add_metric(
                [q.name, JobStatus.SCHEDULED], q.scheduled_job_registry.count
            )

        return rq_jobs_gauge

    def collect(self):
        """Get metrics of the RQ state."""
        with RQPrometheusExporter.summary.time():
            with Connection(self.cache):
                yield self.worker_metrics()
                yield self.queue_metrics()
