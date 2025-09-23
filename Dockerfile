# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-alpine

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock .

RUN pipenv install --system --deploy

COPY . .

RUN crontab crontab

CMD ["crond", "-f", "-l", "2"]
