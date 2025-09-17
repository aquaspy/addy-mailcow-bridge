# Stage 1: Build stage (install dependencies)
FROM python:3.13-slim AS builder

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies in a virtual environment to isolate them
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage (use a minimal image)
FROM python:3.13-slim AS runtime

# Install only runtime essentials (e.g., for potential system calls)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy the virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy your app code (exclude unnecessary files via .dockerignore)
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Activate virtual environment and set PATH
ENV PATH="/opt/venv/bin:$PATH"

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 6510

# Run the app
CMD ["python", "app.py"]
