# 1. Base image (Python)
FROM python:3.12-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Install Poetry
RUN pip install --no-cache-dir poetry

# 4. Copy dependency files first (important for caching)
COPY pyproject.toml poetry.lock* /app/

# 5. Configure Poetry (no virtualenv inside Docker)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# 6. Copy the actual application code
COPY . /app

# 7. Expose FastAPI port
EXPOSE 8000

# 8. Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
