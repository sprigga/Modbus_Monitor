FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
# 原有的端口: 8000
# 修改為5位數冷門端口: 18000
EXPOSE 18000

# Start the application
# 原有的端口: 8000
# 修改為5位數冷門端口: 18000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "18000"]
