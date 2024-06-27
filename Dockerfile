FROM python:3.12.4-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH="/app"

CMD ["fastapi", "run", "src/app/main.py"]
