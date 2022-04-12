FROM python:alpine3.8
COPY . /src
RUN cd /src && \
    pip install .
USER 1000:1000
ENTRYPOINT ["rqmetrics"]
