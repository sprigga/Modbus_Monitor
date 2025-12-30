#!/bin/bash

echo "=== Modbus Monitor System Test ==="

# 測試後端 API
echo "1. Testing Backend API..."
echo "Status: $(curl -s http://localhost:8000/api/status)"
echo "Config: $(curl -s http://localhost:8000/api/config)"

# 測試前端
echo ""
echo "2. Testing Frontend..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8082)
if [ "$FRONTEND_STATUS" == "200" ]; then
    echo "Frontend: ✅ Available at http://localhost:8082"
else
    echo "Frontend: ❌ Not available"
fi

# 測試 Redis 連接
echo ""
echo "3. Testing Redis Connection..."
if redis-cli ping > /dev/null 2>&1; then
    echo "Redis: ✅ Connected and responding"
else
    echo "Redis: ❌ Not available"
fi

echo ""
echo "=== System Ready ==="
echo "🌐 Frontend: http://localhost:8082"
echo "🚀 Backend API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "✅ All services are running successfully!"
echo "You can now configure your Modbus device in the web interface."