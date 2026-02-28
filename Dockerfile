# Stage 1: Builder
FROM python:3.13-slim AS builder

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.13-slim

# Create app user and directories
RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser:appuser /app

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code as appuser
COPY --chown=appuser:appuser . .

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create static/media directories with correct permissions
RUN mkdir -p staticfiles media && \
    chown -R appuser:appuser staticfiles media

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "eventplanner.wsgi:application"]
