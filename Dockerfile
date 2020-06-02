FROM python:3.8-slim-buster

RUN groupadd -r metrics && useradd -r -g metrics metrics

RUN mkdir /app \
    && chown -R metrics:metrics /app

COPY . /app

WORKDIR /app
RUN pip install .[all]
USER metrics

ENTRYPOINT ["rqmetrics"]
