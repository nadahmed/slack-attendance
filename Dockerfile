FROM python:3.9.4-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG uid=1000
ARG gid=1000

RUN addgroup --gid $gid appgroup \
    && adduser --uid $uid --disabled-password --gecos "" --ingroup appgroup appuser

WORKDIR /code

COPY ./requirements.txt .

RUN apk update \
    && apk add --virtual build-deps gcc g++ python3-dev musl-dev \
    && apk add --no-cache \
    freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-deps

COPY . .

RUN chown -R appuser:appgroup /code

USER appuser

# ENTRYPOINT python manage.py collectstatic --no-input && python manage.py runserver 0.0.0.0:$PORT

CMD python manage.py collectstatic --no-input && uvicorn --host 0.0.0.0 --port $PORT slack.asgi:application