#!/bin/bash

# 使用 uv 的 Modbus Monitor 啟動腳本
echo "=== Modbus Monitor - UV Environment Setup ==="

# 檢查是否存在 .env 文件
if [ ! -f .env ]; then
    echo "Creating .env file from .env.new..."
    cp .env.new .env
    echo "Please edit .env file with your Modbus device settings"
fi

# 檢查 Redis 是否運行
if ! redis-cli ping > /dev/null 2>&1; then
    echo "Starting Redis with Docker..."
    docker run -d --name modbus_redis -p 6379:6379 redis:alpine
    sleep 2
fi

# 同步依賴
echo "Syncing dependencies with uv..."
uv sync

# 啟動後端
echo "Starting FastAPI backend with uv..."
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# 等待後端啟動
sleep 5

# 啟動前端 HTTP 服務器
echo "Starting frontend server with uv..."
cd frontend
uv run python -m http.server 8082 &
FRONTEND_PID=$!
cd ..

echo ""
echo "=== Services Started with UV ==="
echo "Frontend: http://localhost:8082"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# 等待中斷信號
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait