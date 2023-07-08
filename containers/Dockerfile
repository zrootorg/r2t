FROM python:3.8-slim-buster

LABEL maintainer="brokenpip3 <brokenpip3@gmail.com>"
LABEL org.opencontainers.image.authors="brokenpip3 <brokenpip3@gmail.com>"
LABEL org.opencontainers.image.title="rtt"
LABEL org.opencontainers.image.description="Rtt docker img: https://github.com/brokenpip3/rtt"
LABEL org.opencontainers.image.url="https://quay.io/brokenpip3/rtt"
LABEL org.opencontainers.image.source="https://github.com/brokenpip3/rtt"
LABEL org.opencontainers.image.base.name="docker.io/python:3.8-slim-buster"

RUN useradd --create-home app
WORKDIR /usr/src/app

USER app
COPY --chown=app rtt/ .
RUN pip install -r requirements.txt --no-cache-dir --user

CMD [ "python", "/usr/src/app/rtt" ]
