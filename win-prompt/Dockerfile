# Use official Python slim image for a significantly smaller attack surface and fast boot times
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirement files first to cache the pip install layer
COPY execution/requirements.txt .

# Install dependencies (no-cache-dir keeps image size small)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the typical port (Cloud Run sets PORT automatically, Render can use 10000)
ENV PORT=8080

# Run the FastAPI server via Uvicorn. Uses Shell execution to parse the $PORT variable dynamically.
CMD ["sh", "-c", "uvicorn orchestration.api:app --host 0.0.0.0 --port ${PORT:-8080}"]
