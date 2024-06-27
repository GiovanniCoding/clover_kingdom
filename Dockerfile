ARG PYTHON_VERSION=3.12.4
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

ENV PYTHONPATH="/app"

CMD ["fastapi", "run", "app/main.py"]
