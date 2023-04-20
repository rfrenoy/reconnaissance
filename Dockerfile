FROM python:3.9

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    cmake \
    build-essential \
    gfortran \
    libgomp1 \
    libopenblas-dev \
    libprotobuf-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Install Python dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Add ~/.local/bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy the application code
COPY server.py /app/

# Set the working directory
WORKDIR /app

# Expose the default port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]