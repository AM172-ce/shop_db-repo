# Use Python 3.9 slim as the base image
FROM python:3.9-slim AS base

# Avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

# Install necessary build tools and libraries
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Set working directory
WORKDIR /code

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install requirements
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Use Python 3.9 slim as the base image for the runner stage
FROM base AS runner

# Create a non-root user
RUN useradd --create-home myuser

# Switch to non-root user
USER myuser

# Expose port 8000
EXPOSE 8000

# Ensure all messages always reach console
ENV PYTHONUNBUFFERED=1

# Activate virtual environment
ENV PATH="/code/venv/bin:$PATH"

# Run the application
CMD ["python", "run_application.py"]

