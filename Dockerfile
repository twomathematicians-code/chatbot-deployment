FROM python:3.11-slim
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --quiet poetry==1.8.3 && poetry config virtualenvs.in-project true && poetry install --only main --no-root
COPY src/ src/
RUN useradd -m -r botuser && chown -R botuser /app && USER botuser
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
