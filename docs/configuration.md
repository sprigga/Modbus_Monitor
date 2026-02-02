# 配置管理系統說明

## 概述

本專案現在使用 pydantic-settings 來管理配置，取代了原本硬編碼的 ModbusConfig 類別。新的配置系統支持從環境變數和 .env 文件中讀取配置。

## 配置文件結構

### 1. 主配置類別 (`backend/config.py`)

#### Settings
主要的配置類別，繼承自 `pydantic_settings.BaseSettings`，包含以下組件：

- **modbus**: Modbus 連接配置
- **redis**: Redis 連接配置
- **api**: API 伺服器配置
- **logging**: 日誌配置

#### ModbusConfig
Modbus 相關的配置，包含：
- host: Modbus 設備 IP 位址
- port: Modbus 埠號 (預設 502)
- device_id: Modbus 設備 ID (預設 1)
- poll_interval: 輪詢間隔 (秒)
- timeout: 超時時間 (秒)
- retries: 重試次數
- register_ranges: 要監控的暫存器範圍列表

#### RedisConfig
Redis 連接配置，包含：
- host: Redis 伺服器位址
- port: Redis 埠號
- password: Redis 密碼 (可選)
- db: 資料庫編號

### 2. 向後相容類別

為了保持向後相容性，原有的 `ModbusConfig` dataclass 仍然存在，但現在有了可配置的預設值：
- `ModbusConfig`: 原始的 dataclass
- `SimpleModbusConfig`: 額外的簡單類別，使用 __init__ 方法

## 配置來源

### 1. 環境變數
配置系統會自動從環境變數中讀取設定，變數名稱以 `MODBUS_` 為前綴：

```bash
# Modbus 設定
MODBUS_HOST=192.168.30.24
MODBUS_PORT=502
MODBUS_DEVICE_ID=1
MODBUS_POLL_INTERVAL=2.0
MODBUS_TIMEOUT=3.0
MODBUS_RETRIES=3

# 暫存器範圍設定
MODBUS_START_ADDRESS=1
MODBUS_END_ADDRESS=26
MODBUS_INPUT_REGISTER_START=100
MODBUS_INPUT_REGISTER_COUNT=8
MODBUS_COILS_START=0
MODBUS_COILS_COUNT=16

# Redis 設定
MODBUS_REDIS_HOST=localhost
MODBUS_REDIS_PORT=6379

# API 設定
MODBUS_API_HOST=0.0.0.0
MODBUS_API_PORT=8000
```

### 2. .env 文件
也可以使用 `.env` 文件來設定環境變數。範例請參考 `.env.example`。

### 3. 預設值
如果沒有設定環境變數，系統會使用預設值。

## 使用方法

### 1. 獲取配置
```python
from backend.config import get_settings

# 獲取配置實例 (會快取)
settings = get_settings()

# 訪問 Modbus 配置
modbus_config = settings.modbus
print(f"Host: {modbus_config.host}")
print(f"Port: {modbus_config.port}")

# 訪問 Redis 配置
redis_config = settings.redis
print(f"Redis Host: {redis_config.host}")

# 訪問暫存器範圍
for reg in settings.modbus.register_ranges:
    print(f"Register {reg.register_type}: {reg.start_address}-{reg.start_address+reg.count-1}")
```

### 2. 在 FastAPI 中使用
```python
# 在 main.py 中已經集成了配置系統
settings = get_settings()

# 初始化 Redis 連接
redis_client = redis.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    password=settings.redis.password,
    db=settings.redis.db,
    decode_responses=True
)

# 初始化 Modbus 服務
modbus_config = settings.modbus
config = ModbusConfig(
    host=modbus_config.host,
    port=modbus_config.port,
    device_id=modbus_config.device_id,
    poll_interval=modbus_config.poll_interval,
    timeout=modbus_config.timeout,
    retries=modbus_config.retries
)
```

### 3. 自訂配置範圍
可以通過環境變數自訂要監控的暫存器範圍：

```bash
# 設定 holding register 範圍
MODBUS_START_ADDRESS=10
MODBUS_END_ADDRESS=50

# 添加 input register 範圍
MODBUS_INPUT_REGISTER_START=100
MODBUS_INPUT_REGISTER_COUNT=16

# 添加 coils 範圍
MODBUS_COILS_START=0
MODBUS_COILS_COUNT=8
```

## 配置驗證

配置系統使用 pydantic 進行自動驗證：
- Port 必須在 1-65535 範圍內
- Device ID 必須在 1-247 範圍內 (Modbus 限制)
- Poll interval 和 timeout 必須大於 0
- Register count 必須在 1-1000 範圍內
- Register type 必須是有效的類型 ('holding', 'input', 'coils', 'discrete_inputs')

## 遷移指南

### 從硬編碼配置遷移
原本的硬編碼配置：
```python
@dataclass
class ModbusConfig:
    host: str
    port: int = 502
    device_id: int = 1
    poll_interval: float = 1.0
    timeout: float = 3.0
    retries: int = 3
```

現在的配置方式：
```python
# 方式 1: 使用環境變數
export MODBUS_HOST=your_host
export MODBUS_PORT=502
export MODBUS_DEVICE_ID=1

# 方式 2: 使用 .env 文件
# 在 .env 文件中設定

# 方式 3: 程式碼中設定
settings = get_settings()
modbus_config = settings.modbus
```

### 獲取配置
```python
# 舊方式
config = ModbusConfig(host="192.168.30.24")

# 新方式
settings = get_settings()
config = settings.modbus
```

## 故障排除

### 1. ModuleNotFoundError: No module named 'pydantic_settings'
確保已安裝 pydantic-settings：
```bash
pip install pydantic-settings
```

### 2. 配置未生效
檢查：
- 環境變數名稱是否正確 (必須以 MODBUS_ 開頭)
- .env 文件是否存在且格式正確
- 是否使用了正確的 Python 環境

### 3. 驗證錯誤
檢查配置值是否符合要求：
- Port 必須在有效範圍內
- Device ID 必須符合 Modbus 規範
- 輪詢間隔必須為正數

## 高級用法

### 1. 動態更新配置
```python
# 在 FastAPI 端點中更新配置
@app.post("/api/config")
async def update_config(config: ModbusConfigModel):
    # 停止當前監控
    if monitoring_task:
        monitoring_task.cancel()

    # 創建新配置
    new_config = ModbusConfig(**config.dict())
    modbus_service = ModbusService(new_config, redis_client)

    return {"message": "Configuration updated"}
```

### 2. 多環境配置
可以創建不同的 .env 文件：
```
.env.development
.env.staging
.env.production
```

然後在啟動應用時指定：
```bash
export MODBUS_ENV=development
python main.py
```