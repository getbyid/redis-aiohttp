FROM python:3.10-slim

RUN pip3 install --no-cache-dir aiohttp redis

COPY app /app

CMD ["python3", "-m", "app"]