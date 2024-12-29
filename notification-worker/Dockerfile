FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /app /app

COPY worker.py /app/

EXPOSE 8000

CMD ["python", "worker.py"]
