
FROM python:3.13-slim

WORKDIR /app

COPY bot/ ./bot/

CMD ["python", "-m", "bot"]
