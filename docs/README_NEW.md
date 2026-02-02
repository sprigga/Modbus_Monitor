# Modbus Monitor - Vue 3 + FastAPI

重構後的 Modbus 監控系統，使用 Vue 3 作為前端，FastAPI 作為後端，Redis 作為數據存儲。

## 架構說明

### Frontend (Vue 3)
- 使用 Vue 3 Composition API
- 響應式 UI 配置 Modbus 連接參數
- 實時數據顯示和監控
- 支持手動讀寫 Holding Registers
- Bootstrap 5 UI 框架

### Backend (FastAPI)
- 基於原有 `async_modbus_monitor.py` 功能
- RESTful API 接口
- 異步 Modbus 通信
- Redis 數據持久化
- WebSocket 支持（可擴展）

### Database (Redis)
- 存儲最新 Modbus 數據
- 歷史數據記錄
- 高性能緩存

## 功能特性

### 1. 配置管理
- 動態配置 Modbus 主機、端口、設備 ID
- 可調整輪詢間隔和超時設置
- 環境變量支持

### 2. 數據監控
- 持續監控 Holding Registers
- 實時數據更新
- 歷史數據查詢
- 自動重連機制

### 3. 讀寫操作
- 支持多種寄存器類型（Holding, Input, Coils, Discrete）
- 單個寄存器寫入
- 批量寄存器寫入
- 手動讀取功能

### 4. 用戶界面
- 直觀的狀態指示器
- 實時數據表格
- 配置表單
- 操作按鈕和警告提示

## 安裝與運行

### 1. 環境準備

```bash
# 安裝 Python 依賴
pip install -r backend/requirements.txt

# 安裝 Redis（Ubuntu/Debian）
sudo apt-get install redis-server

# 或使用 Docker 運行 Redis
docker run -d -p 6379:6379 redis:alpine
```

### 2. 配置環境變量

```bash
# 複製環境配置文件
cp .env.new .env

# 編輯 .env 文件，設置您的 Modbus 設備參數
nano .env
```

### 3. 啟動服務

```bash
# 啟動 Redis（如果沒有使用 Docker）
sudo systemctl start redis

# 啟動 FastAPI 後端
python start_backend.py

# 在瀏覽器中打開前端
# 使用 HTTP 服務器運行前端（例如 Live Server 或 Python HTTP Server）
cd frontend
python -m http.server 8080
```

### 4. 訪問應用

- 前端界面：http://localhost:8080
- API 文檔：http://localhost:8000/docs
- Redis 監控：使用 Redis CLI 或 Redis Desktop Manager

## API 接口

### 配置管理
- `GET /api/config` - 獲取當前配置
- `POST /api/config` - 更新配置

### 連接管理
- `POST /api/connect` - 連接 Modbus 設備
- `POST /api/disconnect` - 斷開連接
- `GET /api/status` - 獲取連接狀態

### 數據操作
- `POST /api/read` - 手動讀取寄存器
- `POST /api/write` - 寫入單個寄存器
- `POST /api/write_multiple` - 寫入多個寄存器

### 監控控制
- `POST /api/start_monitoring` - 開始監控
- `POST /api/stop_monitoring` - 停止監控
- `GET /api/data/latest` - 獲取最新數據
- `GET /api/data/history` - 獲取歷史數據

## 環境變量配置

```bash
# Modbus 設備配置
MODBUS_HOST=192.168.30.24
MODBUS_PORT=502
MODBUS_DEVICE_ID=1

# 輪詢設置
MODBUS_POLL_INTERVAL=2.0
MODBUS_TIMEOUT=3.0
MODBUS_RETRIES=3

# 寄存器範圍
START_ADDRESS=1
END_ADDRESS=26

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379

# API 服務配置
API_HOST=0.0.0.0
API_PORT=8000
```

## 使用說明

### 1. 配置連接
1. 在配置區域輸入 Modbus 設備的 IP 地址和端口
2. 設置設備 ID 和輪詢間隔
3. 點擊 "Update Config" 保存配置

### 2. 建立連接
1. 點擊 "Connect" 按鈕連接到 Modbus 設備
2. 觀察狀態指示器變為綠色（已連接）

### 3. 開始監控
1. 點擊 "Start Monitoring" 開始持續監控
2. 狀態指示器變為黃色閃爍（監控中）
3. 數據表格會顯示實時更新的寄存器值

### 4. 手動操作
1. 使用 "Manual Read" 區域讀取特定寄存器
2. 使用 "Write Holding Register" 區域寫入數據
3. 支持單個和批量寫入操作

## 技術實現

### 前端技術棧
- Vue 3 Composition API
- Axios HTTP 客戶端
- Bootstrap 5 UI 框架
- Font Awesome 圖標

### 後端技術棧
- FastAPI Web 框架
- PyModbus 庫
- Redis 異步客戶端
- Pydantic 數據驗證
- Uvicorn ASGI 服務器

### 數據流程
1. 前端發送 API 請求到 FastAPI 後端
2. 後端使用 PyModbus 與 Modbus 設備通信
3. 數據存儲到 Redis 進行持久化
4. 前端定期輪詢或實時更新數據顯示

## 擴展功能

### 可能的擴展
1. WebSocket 實時數據推送
2. 數據可視化圖表
3. 報警和通知系統
4. 多設備支持
5. 數據導出功能
6. 用戶認證和權限管理

### 性能優化
1. 數據庫查詢優化
2. 緩存策略改進
3. 前端虛擬化大數據集
4. 後端連接池管理

## 故障排除

### 常見問題
1. **無法連接 Modbus 設備**
   - 檢查網絡連接
   - 驗證 IP 地址和端口
   - 確認設備 ID 正確

2. **Redis 連接失敗**
   - 確保 Redis 服務運行
   - 檢查 Redis 配置

3. **前端無法訪問後端**
   - 檢查 CORS 設置
   - 確認 API 地址正確

## 安全考慮

1. 在生產環境中配置適當的 CORS 策略
2. 使用 HTTPS 加密通信
3. 實施認證和授權機制
4. 網絡安全和防火牆配置
5. 定期更新依賴包

## 授權

此項目基於原有 async_modbus_monitor.py 進行重構和擴展。