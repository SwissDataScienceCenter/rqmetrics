# RQ Metrics

[![Actions Status](https://github.com/SwissDataScienceCenter/rq-prometheus-exporter/workflows/rqexport-tests/badge.svg)](https://github.com/SwissDataScienceCenter/rq-prometheus-exporter/actions)


## Install

```
pip install rqmetrics
```

## Getting started

Run it as:

```
rqmetrics
```


or as a container:

```
docker run -it -p 9726:9726 -e RQ_REDIS_HOST=127.0.0.1 rqmetrics:0.1.0
```
