FROM python:3.12.4-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

ENV PYTHONPATH="/app"

CMD ["fastapi", "run", "app/main.py"]
