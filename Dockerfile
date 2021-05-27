FROM python:3.9-alpine

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update && pip install --upgrade pip

COPY ./requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    && apk add libjpeg \
    && apk add  libpq \
    && pip install -r requirements.txt \
    # && pip install Pillow \
    # && pip install psycopg2 \
    && apk del .build-deps

COPY . .

RUN adduser -D dipesh
USER dipesh

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]