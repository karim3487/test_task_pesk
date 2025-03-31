FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy files
COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.cargo/bin:$PATH"

# Default command
CMD ["uvicorn", "test_task_pesk.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
