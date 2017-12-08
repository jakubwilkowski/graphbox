FROM python:3.5-slim

EXPOSE 8000

RUN mkdir /app && \
    apt-get update && \
    apt-get install -y libpq-dev \
    gcc \
    libfreetype6-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng12-dev \
    gettext \
    vim \
    less \
    bash
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD . /app/

ENTRYPOINT /app/manage.py collectstatic --noinput && \
           /app/manage.py migrate && \
           /app/manage.py runserver 0.0.0.0:8000
