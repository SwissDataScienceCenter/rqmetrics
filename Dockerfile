FROM python:3.8-slim-buster

RUN mkdir /app \
    && chown -R 1000:1000 /app

COPY . /app

WORKDIR /app
RUN pip install .[all]
USER 1000:1000

ENTRYPOINT ["rqmetrics"]
