FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml README.md ./
COPY app ./app
COPY data ./data
COPY scripts ./scripts
RUN pip install --no-cache-dir .
RUN mkdir -p /app/data
EXPOSE 8000
CMD ["sh", "-c", "python -m scripts.seed && exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
