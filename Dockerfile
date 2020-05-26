FROM python:3.8-slim-buster

RUN groupadd -r metrics && useradd -r -g metrics metrics
USER metrics
COPY . /app

RUN mkdir /app \
    && chown -R metrics:metrics /app

WORKDIR /app
RUN pipenv install 

ENTRYPOINT ["python", "-m", "rqexport"]
