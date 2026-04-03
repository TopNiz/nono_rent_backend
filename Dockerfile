FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Copy pyproject.toml and uv.lock
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-install-project --no-dev

# Copy source code
COPY src/ ./src/

# Default persistent SQLite path (can be overridden)
ENV DATABASE_URL=sqlite:///./data/app.db

# Ensure sqlite directory exists for mounted volumes
RUN mkdir -p /app/data

# Persist database directory
VOLUME ["/app/data"]

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "fastapi", "run", "src/nono_rent_backend/main.py", "--host", "0.0.0.0", "--port", "8000"]
