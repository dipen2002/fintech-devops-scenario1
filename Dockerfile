# ==============================================================================
# FinTechFlow - Production Multi-stage / Minimal Dockerfile
# ==============================================================================
# Base Image: Small, secure, official Python 3.12 slim distribution
# Security: Runs under a non-privileged dedicated system user (appuser:10001)
# ==============================================================================

FROM python:3.12-slim

# Set environment variables for Python runtime optimization
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    ENVIRONMENT=production

# Set secure working directory
WORKDIR /app

# Create a dedicated non-root user and group with specific UID/GID
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /sbin/nologin -d /app appuser

# Install production dependencies first (optimized layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/
COPY pyproject.toml .

# Assign explicit ownership to the non-root application user
RUN chown -R appuser:appgroup /app

# Switch context to non-root user
USER appuser

# Expose HTTP port
EXPOSE 5000

# Automated Docker container healthcheck using Python standard library (no extra tools needed)
HEALTHCHECK --interval=20s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:5000/health').getcode() == 200 else 1)"

# Start production WSGI server with structured logging to stdout/stderr
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--access-logfile", "-", "--error-logfile", "-", "app:create_app()"]
