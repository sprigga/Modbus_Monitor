# Async Modbus Monitor

一個基於 Python asyncio 的異步 Modbus 數據監控系統,提供 CLI 工具、FastAPI 後端服務和 Vue 3 前端界面,支持完整的 Modbus TCP 讀寫操作。

## 📋 專案概述

本專案是一個全端 (Full-stack) Modbus 監控解決方案,包含:
- **核心 Python 模組**: 異步 Modbus 客戶端庫  
- **CLI 工具**: 命令列監控與讀寫工具
- **REST API 後端**: FastAPI 服務器,提供 HTTP 接口
- **Web 前端**: Vue 3 現代化用戶界面
- **數據存儲**: Redis 時序數據儲存
- **容器化部署**: Docker Compose 一鍵部署

## 🖼️ 系統截圖

以下是系統的主要界面截圖，展示了 Web 前端界面的完整功能：

### 1. Web 前端 - 配置與連接控制界面
![Web Frontend Configuration](screenshot/image1.png)
*現代化的 Vue 3 界面，採用玻璃擬態 (Glass-morphism) 設計風格。包含完整的 Modbus 配置面板 (Host、Port、Device ID、Poll Interval、地址範圍) 和連接控制按鈕 (Update Config、Connect、Disconnect、Start/Stop Monitoring)，右上角顯示即時連接狀態*

### 2. Web 前端 - 手動讀取界面
![Web Frontend Manual Read](screenshot/image2.png)
*手動讀取 (Manual Read) 功能區，可指定寄存器地址 (Address)、讀取數量 (Count) 和寄存器類型 (Register Type: Holding/Input/Coils/Discrete Inputs)。下方為寫入 Holding Register 區域，支援單一值或多值 (逗號分隔) 寫入。右側顯示讀取成功的通知訊息，展示讀回的數值*

### 3. Web 前端 - 寫入測試與數據監控界面
![Web Frontend Write and Monitor](screenshot/image3.png)
*展示完整的寫入與監控流程。上方為 Write Holding Register 區域，包含單一寫入和多值寫入按鈕 (Write Single/Write Multiple)。下方 Modbus Data 表格即時顯示監控數據，包含寄存器名稱 (Name)、地址 (Address)、類型 (Type)、數值 (Values) 和時間戳 (Timestamp)。右側綠色通知顯示多次讀取成功的結果*

### 4. API 文檔界面
瀏覽器訪問 `http://localhost:8000/docs` 可查看完整的 Swagger UI 交互式 API 文檔，方便開發者快速測試所有端點 (連接、讀取、寫入、監控、數據查詢等)

## 📁 專案結構分析

### 核心文件概覽

```
modbus_test/
├── async_modbus_monitor.py    (377行) - 核心 Modbus 監控模組
├── example_config.py           (492行) - CLI 配置示例與互動式工具  
├── start_backend.py            (28行)  - 後端啟動腳本
├── backend/
│   ├── main.py                 (332行) - FastAPI REST API 服務
│   └── modbus_service.py       (297行) - Modbus 服務整合 Redis
├── frontend/
│   ├── index.html              (518行) - Vue 3 前端界面
│   ├── app.js                  - 前端應用邏輯  
│   └── css/styles.css          - 漸層玻璃風格 UI
├── docker-compose.yml          - Docker 容器編排
├── Dockerfile.backend          - 後端容器映像
├── pyproject.toml              - UV 專案配置
├── requirements.txt            - Python 依賴套件
├── .env.example                - 環境變數範例
├── CLAUDE.md                   - 開發指引
├── USAGE.md                    - 使用說明
└── REFACTOR_SUMMARY.md         - 重構記錄
```

**總計程式碼**: 約 1,522 行 Python 代碼

### 文件功能說明

#### 核心模組 (Core Modules)
- **async_modbus_monitor.py**: 獨立的異步 Modbus 客戶端庫,可單獨使用或作為其他模組的基礎
- **example_config.py**: CLI 工具,支持讀取/寫入/監控三種模式,從 .env 或 config.conf 載入配置

#### 後端服務 (Backend Services)  
- **backend/main.py**: FastAPI 應用主程序,提供 RESTful API 端點
- **backend/modbus_service.py**: 擴展核心 Monitor 類,整合 Redis 數據存儲功能
- **start_backend.py**: 後端服務啟動腳本,使用 uvicorn

#### 前端應用 (Frontend Application)
- **frontend/index.html**: Vue 3 單頁應用,玻璃擬態設計風格
- **frontend/app.js**: Vue 應用邏輯,處理 API 通信與狀態管理
- **frontend/css/styles.css**: 響應式 CSS,現代化漸層效果

#### 配置與部署 (Configuration & Deployment)
- **pyproject.toml**: UV 專案配置,定義依賴和構建設置
- **docker-compose.yml**: 三容器架構 (Redis + Backend + Frontend)
- **Dockerfile.backend**: FastAPI 服務容器映像定義

## 🏗️ 系統架構

### 三層架構設計

```
┌─────────────────────────────────────────────────────────┐
│                  Web Frontend (Vue 3)                    │
│              Modern Glass-Morphism UI                    │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST API
┌────────────────────▼────────────────────────────────────┐
│              FastAPI Backend Service                     │
│          (Async HTTP Server + WebSocket)                 │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │                         │
┌───────▼────────┐     ┌─────────▼──────────┐
│  Modbus Service│     │   Redis Database    │
│  (TCP Client)  │     │  (Time-Series Data) │
└───────┬────────┘     └────────────────────┘
        │
┌───────▼────────────────────────┐
│    Modbus TCP Devices           │
│  (PLC, Sensors, Controllers)    │
└────────────────────────────────┘
```

### 核心類別結構

#### 1. ModbusConfig - Modbus 連接配置
位置: `async_modbus_monitor.py:18-25`

```python
@dataclass  
class ModbusConfig:
    host: str                    # Modbus 設備 IP 地址
    port: int = 502             # 端口號 (默認 502)
    device_id: int = 1          # 設備 ID (從站 ID)  
    poll_interval: float = 1.0  # 輪詢間隔 (秒)
    timeout: float = 3.0        # 超時時間 (秒)
    retries: int = 3            # 重試次數
```

#### 2. RegisterConfig - 寄存器配置  
位置: `async_modbus_monitor.py:28-34`

```python
@dataclass
class RegisterConfig:
    address: int                           # 寄存器地址
    count: int = 1                        # 讀取數量
    register_type: str = 'holding'        # 寄存器類型
    name: str = None                      # 寄存器名稱
```

#### 3. AsyncModbusMonitor - 核心監控類
位置: `async_modbus_monitor.py:37-298` (377行)

**主要功能模組**:

| 功能類別 | 方法 | 行數 | 說明 |
|---------|------|------|------|
| 連接管理 | `connect()` | 58-79 | 建立 Modbus TCP 連接 |
|         | `disconnect()` | 81-85 | 斷開連接並清理資源 |
| 讀取操作 | `read_register()` | 87-146 | 讀取單個寄存器配置 |
|         | `read_all_registers()` | 148-160 | 並發讀取所有配置的寄存器 |
| 寫入操作 | `write_holding_register()` | 162-196 | 寫入單個保持寄存器 |
|         | `write_holding_registers()` | 198-234 | 寫入多個保持寄存器 |
| 監控功能 | `monitor_continuously()` | 236-286 | 持續監控循環 |
|         | `add_register()` | 47-56 | 添加寄存器到監控列表 |
| 輔助功能 | `log_data()` | 288-294 | 數據日誌輸出 |
|         | `stop()` | 296-298 | 停止監控 |

**關鍵技術實現**:
- 使用 `AsyncModbusTcpClient` 實現異步通信
- `asyncio.gather()` 實現並發寄存器讀取
- 自動重連機制 (最大連續錯誤 5 次)
- 支持 4 種寄存器類型 (Holding, Input, Coils, Discrete Inputs)

#### 4. ModbusService - 後端服務類
位置: `backend/modbus_service.py:39-297` (297行)

**擴展功能**:

| 功能 | 方法 | 說明 |
|------|------|------|
| Redis 整合 | `store_data_to_redis()` | 存儲最新數據和歷史記錄 |
| 連接狀態 | `is_connected()` | 檢查連接狀態 |
| 監控服務 | `start_monitoring()` | 帶 Redis 存儲的監控循環 |
| 格式化讀取 | `read_registers()` | 返回 REST API 格式的數據 |

**Redis 數據結構**:
- `modbus:latest` - String, 存儲最新數據 JSON
- `modbus:history` - Sorted Set, 時間戳為分數,保留最近 1000 筆

## 🎯 技術特點分析

### 異步架構  
- **事件循環**: 基於 `asyncio` 事件循環實現
- **非阻塞 I/O**: 所有網絡操作使用 async/await
- **並發處理**: `asyncio.gather()` 並發執行多個任務
- **性能優勢**: 單執行緒處理數百個並發連接

### 錯誤處理與容錯

#### 連接層級 (async_modbus_monitor.py:236-286)
```python
consecutive_errors = 0
max_consecutive_errors = 5

while self.running:
    if not self.client.connected:
        if not await self.connect():
            consecutive_errors += 1
            if consecutive_errors >= max_consecutive_errors:
                break  # 超過限制則停止
```

#### 讀取層級  
- 捕獲 `ModbusException` 異常
- 捕獲通用 `Exception` 異常  
- 詳細錯誤日誌記錄
- 返回 None 而不是拋出異常

### 數據處理能力

#### CLI 模式 (example_config.py:129-173)
```python
async def data_processor(data):
    """支持十六進制和十進制顯示"""
    for item in data:
        # 顯示每個寄存器的地址、十六進制和十進制值
        for i, value in enumerate(values):
            current_addr = address + i  
            print(f"{current_addr:<12} 0x{value:04X}      {value:<15}")
        
        # 統計計算
        avg = sum(values) / len(values)
        max_val = max(values)
        min_val = min(values)
```

#### API 模式 (backend/main.py)
- Pydantic 模型驗證
- JSON 序列化輸出
- 時間戳標準化 (ISO 8601)

### Web 前端特色

#### Vue 3 響應式設計 (frontend/index.html)
```javascript
// Composition API 風格
data() {
    return {
        config: {...},      // 配置狀態
        status: {...},      // 連接狀態  
        latestData: null,   // 最新數據
        autoRefresh: false  // 自動刷新開關
    }
}
```

#### 玻璃擬態 UI (frontend/css/styles.css)
```css
.glass-card {
    background: var(--background-glass);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-color);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
```

## 🚀 功能特點

### 1. 完整的 Modbus 操作

#### 支持的寄存器類型

| 類型 | Modbus 功能碼 | 讀取 | 寫入 | 數據類型 | 典型用途 |
|------|--------------|------|------|----------|----------|
| Holding Registers | FC03, FC06, FC16 | ✅ | ✅ | 16-bit | 設定值、參數配置 |
| Input Registers | FC04 | ✅ | ❌ | 16-bit | 傳感器讀數 |
| Coils | FC01, FC05, FC15 | ✅ | ✅ | 1-bit | 數字輸出控制 |
| Discrete Inputs | FC02 | ✅ | ❌ | 1-bit | 開關狀態、報警 |

#### 讀取操作實現 (async_modbus_monitor.py:87-146)
```python
async def read_register(self, reg_config: RegisterConfig):
    if reg_config.register_type == 'holding':
        result = await self.client.read_holding_registers(
            reg_config.address, 
            count=reg_config.count,
            device_id=self.config.device_id
        )
    # ... 其他類型類似實現
```

#### 寫入操作實現 (async_modbus_monitor.py:162-234)
- **單寄存器寫入**: `write_register()` - FC06  
- **多寄存器寫入**: `write_registers()` - FC16
- 支持十六進制和十進制輸入
- 寫入前後驗證讀取

### 2. 三種使用模式

#### A. CLI 命令列模式

**基本用法** (example_config.py:302-492):

```bash
# 1. 純讀取監控模式
uv run python example_config.py

# 2. 寫入單個寄存器  
uv run python example_config.py --write --address 10 --values 1234

# 3. 寫入多個寄存器 (十進制)
uv run python example_config.py --write --address 10 --values 100,200,300

# 4. 寫入多個寄存器 (十六進制)
uv run python example_config.py --write --address 10 --values 0x64,0xC8,0x12C

# 5. 互動式寫入模式
uv run python example_config.py --write-interactive

# 6. 寫入後繼續監控
uv run python example_config.py --write --address 10 --values 1234 --monitor
```

**互動式寫入功能** (example_config.py:175-277):
```
Enter register address (or 'q' to quit): 10
Enter value(s) (comma-separated, hex with 0x): 0x3C,0x64
Confirm write? (y/n): y
✅ Write operation completed!
Read back to verify? (y/n): y
```

#### B. REST API 模式

**啟動後端服務**:
```bash
# 方式 1: 使用 start_backend.py
uv run python start_backend.py

# 方式 2: 直接使用 uvicorn  
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**API 端點列表** (backend/main.py:64-330):

| 端點 | 方法 | 功能 | 請求體 |
|------|------|------|--------|
| `/api/config` | GET | 獲取配置 | - |
| `/api/config` | POST | 更新配置 | ModbusConfigModel |
| `/api/connect` | POST | 連接設備 | - |
| `/api/disconnect` | POST | 斷開連接 | - |
| `/api/status` | GET | 獲取狀態 | - |
| `/api/read` | POST | 讀取寄存器 | RegisterReadRequest |
| `/api/write` | POST | 寫入單個寄存器 | RegisterWriteRequest |
| `/api/write_multiple` | POST | 寫入多個寄存器 | MultipleRegisterWriteRequest |
| `/api/start_monitoring` | POST | 開始監控 | - |
| `/api/stop_monitoring` | POST | 停止監控 | - |
| `/api/data/latest` | GET | 獲取最新數據 | - |
| `/api/data/history` | GET | 獲取歷史數據 | limit (query param) |

**API 使用範例**:
```bash
# 連接設備
curl -X POST http://localhost:8000/api/connect

# 讀取寄存器
curl -X POST http://localhost:8000/api/read \
  -H "Content-Type: application/json" \
  -d '{"address": 0, "count": 10, "register_type": "holding"}'

# 寫入寄存器
curl -X POST http://localhost:8000/api/write \
  -H "Content-Type: application/json" \
  -d '{"address": 10, "value": 1234}'

# 獲取最新數據
curl http://localhost:8000/api/data/latest
```

#### C. Web 界面模式

**訪問方式**: `http://localhost:8081`

**界面功能** (frontend/index.html):
1. **配置面板**: 動態修改 Modbus 連接參數
2. **連接控制**: Connect/Disconnect/Start Monitoring/Stop 按鈕
3. **手動讀取**: 指定地址、數量和寄存器類型讀取
4. **寫入操作**: 單個或多個寄存器寫入
5. **數據顯示**: 表格形式實時顯示監控數據
6. **自動刷新**: 可開啟/暫停自動數據更新
7. **狀態指示**: 連接狀態和監控狀態的視覺指示

### 3. 靈活的配置管理

#### 配置優先級 (example_config.py:92-127)

```python
def load_config():
    """
    配置來源優先級:
    1. .env 文件 (最高)
    2. config.conf 文件  
    3. 硬編碼默認值 (最低)
    """
    config = load_config_from_env()
    if config: return config
    
    config = load_config_from_conf()  
    if config: return config
    
    return default_config  # 硬編碼默認值
```

#### .env 文件格式 (.env.example)
```bash
# Modbus 設備網絡配置
MODBUS_HOST=192.168.30.24
MODBUS_PORT=502
MODBUS_DEVICE_ID=1

# 輪詢和超時設置
MODBUS_POLL_INTERVAL=2.0
MODBUS_TIMEOUT=3.0
MODBUS_RETRIES=3

# 寄存器範圍配置
START_ADDRESS=1
END_ADDRESS=26

# 日誌級別
LOG_LEVEL=INFO
```

## 📦 依賴項分析

### Python 依賴 (pyproject.toml)

#### 核心依賴
```toml
[project.dependencies]
pymodbus = ">=3.0.0"        # Modbus 協議實現, ~50KB
python-dotenv = ">=1.0.0"   # 環境變數管理, ~20KB
```

#### 後端專用依賴  
```toml
fastapi = ">=0.104.0"             # Web 框架, ~300KB
uvicorn[standard] = ">=0.24.0"    # ASGI 伺服器, ~200KB
redis = ">=5.0.0"                 # Redis 客戶端, ~150KB
pydantic = ">=2.0.0"              # 數據驗證, ~400KB
python-multipart = ">=0.0.6"      # 表單處理, ~30KB
```

#### 標準庫 (無需安裝)
```python
import asyncio       # 異步 I/O
import logging       # 日誌記錄
import datetime      # 時間處理
import json          # JSON 序列化
import typing        # 類型提示
import dataclasses   # 數據類
import configparser  # INI 配置解析
import argparse      # 命令列參數解析
```

### 系統依賴

- **Python**: >= 3.10 (使用 match-case 和新型類型提示)
- **Redis**: >= 7.0 (用於時序數據存儲)
- **UV**: Python 套件管理工具 (推薦, 比 pip 快 10-100 倍)
- **Docker**: >= 20.10 (可選, 用於容器化部署)

### 前端依賴 (CDN 載入)

```html
<!-- Vue 3 框架 -->
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>

<!-- Axios HTTP 客戶端 -->  
<script src="https://unpkg.com/axios/dist/axios.min.js"></script>

<!-- Font Awesome 圖標 -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
```

## 🔧 安裝與設置

### 方法一: 使用 UV (推薦)

```bash
# 1. 安裝 UV (如果未安裝)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 克隆專案
git clone <repository-url>
cd modbus_test

# 3. 使用 UV 同步依賴
uv sync

# 4. 配置環境變數
cp .env.example .env
nano .env  # 編輯配置

# 5. 啟動 Redis (如果使用後端)
docker run -d -p 6379:6379 --name modbus-redis redis:7-alpine

# 6. 運行 CLI 工具
uv run python example_config.py

# 7. 啟動後端服務 (可選)
uv run python start_backend.py
```

### 方法二: 使用 Docker Compose

```bash
# 1. 配置環境變數
cp .env.example .env
nano .env  # 修改 MODBUS_HOST 等參數

# 2. 啟動所有服務 (一鍵部署)
docker-compose up -d

# 3. 查看服務狀態
docker-compose ps

# 4. 查看日誌
docker-compose logs -f backend

# 5. 訪問服務
# - Web 前端: http://localhost:8081
# - API 文檔: http://localhost:8000/docs  
# - Redis: localhost:6380

# 6. 停止服務
docker-compose down
```

### 方法三: 傳統 pip 安裝

```bash
# 1. 創建虛擬環境
python3 -m venv venv

# 2. 激活虛擬環境
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate   # Windows

# 3. 升級 pip
pip install --upgrade pip

# 4. 安裝依賴
pip install -r requirements.txt

# 5. 配置環境  
cp .env.example .env

# 6. 運行程序
python example_config.py
```

## 💡 使用範例

### 範例 1: 基本讀取監控

檔案: `examples/basic_read.py`

```python
from async_modbus_monitor import AsyncModbusMonitor, ModbusConfig
import asyncio
import logging

async def main():
    # 配置日誌
    logging.basicConfig(level=logging.INFO)
    
    # 配置連接
    config = ModbusConfig(
        host='192.168.1.100',
        port=502,
        device_id=1,
        poll_interval=2.0,
        timeout=5.0
    )

    # 創建監控器
    monitor = AsyncModbusMonitor(config)

    # 添加要監控的寄存器
    monitor.add_register(
        address=0,           # 起始地址
        count=10,           # 讀取 10 個寄存器
        register_type='holding',
        name='Temperature_Setpoints'
    )
    
    monitor.add_register(
        address=100,
        count=5,
        register_type='input',
        name='Sensor_Readings'
    )

    try:
        # 連接設備
        if await monitor.connect():
            print("✅ 連接成功!")
            
            # 開始持續監控
            await monitor.monitor_continuously()
    except KeyboardInterrupt:
        print("\n⏹️  停止監控...")
        monitor.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### 範例 2: 寫入寄存器

檔案: `examples/write_registers.py`

```python
from async_modbus_monitor import AsyncModbusMonitor, ModbusConfig, RegisterConfig
import asyncio

async def write_example():
    config = ModbusConfig(host='192.168.1.100')
    monitor = AsyncModbusMonitor(config)

    if await monitor.connect():
        print("已連接到 Modbus 設備")
        
        # 寫入單個寄存器
        success = await monitor.write_holding_register(
            address=10,
            value=1234
        )
        print(f"寫入單個寄存器: {'成功' if success else '失敗'}")
        
        # 寫入多個寄存器
        success = await monitor.write_holding_registers(
            address=20,
            values=[100, 200, 300, 400, 500]
        )
        print(f"寫入多個寄存器: {'成功' if success else '失敗'}")
        
        # 讀取驗證
        reg_config = RegisterConfig(
            address=10,
            count=1,
            register_type='holding'
        )
        result = await monitor.read_register(reg_config)
        if result:
            print(f"驗證讀取: 地址 10 = {result['values'][0]}")
        
        await monitor.disconnect()

asyncio.run(write_example())
```

### 範例 3: 自定義數據處理

檔案: `examples/custom_processor.py`

```python
from async_modbus_monitor import AsyncModbusMonitor, ModbusConfig
import asyncio
from typing import List, Dict, Any

async def temperature_processor(data: List[Dict[str, Any]]):
    """溫度數據處理器 - 轉換為攝氏度"""
    print(f"\n{'='*60}")
    print(f"📊 溫度監控報告 - {len(data)} 個讀數")
    print(f"{'='*60}")
    
    for item in data:
        name = item['name']
        raw_values = item['values']
        
        # 假設原始值需要除以 10 得到實際溫度
        temperatures = [v / 10.0 for v in raw_values]
        
        # 統計分析
        avg_temp = sum(temperatures) / len(temperatures)
        max_temp = max(temperatures)
        min_temp = min(temperatures)
        
        print(f"\n🌡️  {name}:")
        print(f"   溫度範圍: {temperatures}")
        print(f"   平均溫度: {avg_temp:.1f}°C")
        print(f"   最高溫度: {max_temp:.1f}°C")
        print(f"   最低溫度: {min_temp:.1f}°C")
        
        # 報警檢查
        if max_temp > 80.0:
            print(f"   ⚠️  警告: 溫度過高!")
        elif max_temp > 70.0:
            print(f"   ⚡ 注意: 溫度偏高")

async def main():
    config = ModbusConfig(
        host='192.168.1.100',
        poll_interval=5.0  # 每 5 秒更新一次
    )
    
    monitor = AsyncModbusMonitor(config)
    monitor.add_register(0, 8, 'input', '爐溫傳感器')
    monitor.add_register(100, 4, 'input', '環境溫度')
    
    if await monitor.connect():
        # 使用自定義處理器
        await monitor.monitor_continuously(
            data_callback=temperature_processor
        )

asyncio.run(main())
```

### 範例 4: 多設備監控

檔案: `examples/multi_device.py`

```python
import asyncio
from async_modbus_monitor import AsyncModbusMonitor, ModbusConfig

async def monitor_device(device_name: str, host: str):
    """監控單個設備"""
    config = ModbusConfig(host=host, poll_interval=2.0)
    monitor = AsyncModbusMonitor(config)
    
    monitor.add_register(0, 10, 'holding', f'{device_name}_Holdings')
    
    if await monitor.connect():
        print(f"✅ {device_name} 已連接")
        
        async def device_callback(data):
            for item in data:
                print(f"[{device_name}] {item['name']}: {item['values']}")
        
        await monitor.monitor_continuously(data_callback=device_callback)

async def main():
    """並發監控多個設備"""
    devices = [
        ("PLC-1", "192.168.1.100"),
        ("PLC-2", "192.168.1.101"),
        ("PLC-3", "192.168.1.102"),
    ]
    
    # 並發執行多個監控任務
    tasks = [monitor_device(name, host) for name, host in devices]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔐 安全注意事項

### 生產環境部署檢查清單

#### 1. 網絡安全
- [ ] 使用防火牆限制 Modbus 端口 (502) 訪問
- [ ] 將 Modbus 設備隔離到專用 VLAN
- [ ] 使用 VPN 進行遠程訪問
- [ ] 禁用不必要的服務和端口

#### 2. API 安全 (backend/main.py 需修改)

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """JWT Token 驗證"""
    token = credentials.credentials
    # 實現 token 驗證邏輯
    if not validate_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# 受保護的端點
@app.post("/api/write", dependencies=[Depends(verify_token)])
async def write_register(...):
    pass
```

#### 3. CORS 配置

```python
# 生產環境應限制允許的來源
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-domain.com",
        "https://app.your-domain.com"
    ],  # 替換為實際域名
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # 限制允許的方法
    allow_headers=["Authorization", "Content-Type"],
)
```

#### 4. 環境變數管理

```bash
# 不要將敏感信息提交到版本控制
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore

# 使用密鑰管理服務
# AWS: Secrets Manager
# Azure: Key Vault  
# GCP: Secret Manager
```

#### 5. 速率限制

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/write")
@limiter.limit("10/minute")  # 每分鐘最多 10 次寫入
async def write_register(...):
    pass
```

#### 6. 審計日誌

```python
import logging
from datetime import datetime

# 記錄所有寫入操作
async def log_write_operation(user: str, address: int, value: int):
    logging.info(
        f"WRITE_AUDIT: user={user}, address={address}, "
        f"value={value}, timestamp={datetime.now().isoformat()}"
    )

@app.post("/api/write")
async def write_register(request: RegisterWriteRequest, user=Depends(get_current_user)):
    await log_write_operation(user.username, request.address, request.value)
    # ... 執行寫入
```

#### 7. HTTPS 配置

```bash
# 使用 Let's Encrypt 獲取免費 SSL 證書
certbot certonly --standalone -d your-domain.com

# Nginx 反向代理配置
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

## 🔧 故障排除

### 問題 1: 連接失敗

**錯誤訊息**:
```
Failed to connect to Modbus device
Connection error: [Errno 113] No route to host
```

**診斷步驟**:
```bash
# 1. 測試網絡連通性
ping 192.168.1.100

# 2. 測試端口連通性
nc -zv 192.168.1.100 502

# 3. 檢查防火牆
sudo iptables -L -n | grep 502

# 4. 查看設備日誌
uv run python example_config.py 2>&1 | tee modbus.log
```

**解決方案**:
- 確認 IP 地址正確
- 檢查設備是否啟用 Modbus TCP
- 調整防火牆規則允許 502 端口
- 增加 timeout 參數: `timeout=10.0`

### 問題 2: 讀取錯誤

**錯誤訊息**:
```
Error reading Holding_0-9: Modbus Error: [Input/Output] Modbus Error: [Invalid Message] Incomplete message received, expected at least 8 bytes
```

**診斷**:
```python
# 啟用詳細日誌
logging.getLogger('pymodbus').setLevel(logging.DEBUG)

# 單個寄存器測試
monitor.add_register(0, 1, 'holding', 'Test_Single')
```

**解決方案**:
- 減少 count 數量 (某些設備限制單次讀取數量)
- 驗證寄存器地址是否存在
- 檢查 device_id 是否正確
- 確認寄存器類型 (holding vs input)

### 問題 3: Redis 連接失敗

**錯誤訊息**:
```
redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379. Connection refused.
```

**解決方案**:
```bash
# 檢查 Redis 是否運行
redis-cli ping

# 如果未運行,啟動 Redis
docker run -d -p 6379:6379 redis:7-alpine

# 或使用系統服務
sudo systemctl start redis
sudo systemctl enable redis

# 檢查 Redis 版本
redis-cli INFO server | grep redis_version
```

### 問題 4: 性能問題

**症狀**: 數據更新緩慢,CPU 使用率高

**性能分析**:
```python
import cProfile
import pstats

# 性能分析
profiler = cProfile.Profile()
profiler.enable()

await monitor.monitor_continuously()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

**優化建議**:
```python
# 1. 增加輪詢間隔
config = ModbusConfig(poll_interval=5.0)  # 從 1.0 增加到 5.0

# 2. 減少並發讀取數量
monitor.add_register(0, 10, 'holding')  # 改為分批讀取
monitor.add_register(10, 10, 'holding')

# 3. 使用連接池 (多設備場景)
# 4. 啟用 Redis 持久化優化
```

### 問題 5: Docker 容器問題

**錯誤**: 容器無法啟動

```bash
# 查看容器日誌
docker-compose logs backend

# 重建容器
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# 進入容器調試
docker-compose exec backend /bin/bash

# 檢查網絡
docker network inspect modbus_test_default
```

## 📚 API 文檔

### REST API 詳細說明

FastAPI 自動生成交互式 API 文檔:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### API 請求/響應範例

#### 1. 連接設備

**請求**:
```http
POST /api/connect HTTP/1.1
Content-Type: application/json
```

**響應**:
```json
{
  "message": "Connected successfully"
}
```

#### 2. 讀取寄存器

**請求**:
```http
POST /api/read HTTP/1.1
Content-Type: application/json

{
  "address": 0,
  "count": 10,
  "register_type": "holding"
}
```

**響應**:
```json
{
  "address": 0,
  "type": "holding",
  "count": 10,
  "values": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
  "timestamp": "2025-11-07T10:30:45.123456"
}
```

#### 3. 寫入寄存器

**請求**:
```http
POST /api/write HTTP/1.1
Content-Type: application/json

{
  "address": 10,
  "value": 1234
}
```

**響應**:
```json
{
  "message": "Successfully wrote value 1234 to address 10"
}
```

#### 4. 獲取最新數據

**請求**:
```http
GET /api/data/latest HTTP/1.1
```

**響應**:
```json
{
  "data": [
    {
      "name": "Holding_1-26",
      "address": 1,
      "type": "holding",
      "values": [15418, 15419, ...],
      "timestamp": "2025-11-07T10:30:45.123456"
    }
  ],
  "timestamp": "2025-11-07T10:30:45.123456"
}
```

## 📝 開發指導原則

### 代碼修改規範 (根據 CLAUDE.md)

#### 1. 使用 UV 管理 Python 環境
```bash
# ✅ 正確: 使用 uv run
uv run python script.py
uv run pytest tests/

# ❌ 錯誤: 直接使用 python
python script.py
```

#### 2. 保留原始代碼,使用註釋標記

**範例: 修改函數**:
```python
# ===== 原有程式碼 (COMMENTED OUT - 2025-11-07) =====
# def process_data(data):
#     """原始實現 - 同步處理"""
#     result = []
#     for item in data:
#         result.append(transform(item))
#     return result

# ===== 新程式碼 (UPDATED - 2025-11-07) =====  
# 修改原因: 改為異步實現以提升性能
async def process_data(data):
    """異步處理多個數據項"""
    tasks = [transform_async(item) for item in data]
    return await asyncio.gather(*tasks)
```

**範例: 修改配置**:
```python
# ===== 原有配置 (COMMENTED OUT - 使用 config.conf) =====
# config = ModbusConfig(
#     host='192.168.30.24',
#     port=502,
#     device_id=1,
#     poll_interval=2.0
# )

# ===== 新配置 (UPDATED - 從 .env 載入) =====
# 修改原因: 支持環境變數配置,更靈活
config = ModbusConfig(
    host=os.getenv('MODBUS_HOST', '192.168.30.24'),
    port=int(os.getenv('MODBUS_PORT', 502)),
    device_id=int(os.getenv('MODBUS_DEVICE_ID', 1)),
    poll_interval=float(os.getenv('MODBUS_POLL_INTERVAL', 2.0))
)
```

### 代碼風格指南

#### 類型提示
```python
from typing import List, Dict, Any, Optional

async def read_multiple_registers(
    addresses: List[int],
    counts: List[int],
    register_type: str = 'holding'
) -> List[Optional[Dict[str, Any]]]:
    """完整的類型提示"""
    pass
```

#### Docstring 格式
```python
async def write_holding_register(self, address: int, value: int) -> bool:
    """
    Write a single holding register
    
    Args:
        address: Register address to write to
        value: Value to write (0-65535 for single register)
    
    Returns:
        True if write successful, False otherwise
    
    Raises:
        ModbusException: If communication error occurs
    
    Example:
        >>> monitor = AsyncModbusMonitor(config)
        >>> await monitor.connect()
        >>> success = await monitor.write_holding_register(10, 1234)
    """
    pass
```

### 測試指南

#### 單元測試範例
```python
# tests/test_modbus_monitor.py
import pytest
from async_modbus_monitor import AsyncModbusMonitor, ModbusConfig

@pytest.mark.asyncio
async def test_connect_success():
    """測試成功連接"""
    config = ModbusConfig(host='localhost', port=5020)
    monitor = AsyncModbusMonitor(config)
    
    result = await monitor.connect()
    assert result == True
    assert monitor.client.connected == True
    
    await monitor.disconnect()

@pytest.mark.asyncio  
async def test_read_holding_registers():
    """測試讀取 Holding Registers"""
    config = ModbusConfig(host='localhost')
    monitor = AsyncModbusMonitor(config)
    
    await monitor.connect()
    monitor.add_register(0, 10, 'holding', 'Test')
    
    data = await monitor.read_all_registers()
    assert len(data) == 1
    assert data[0]['name'] == 'Test'
    assert len(data[0]['values']) == 10
```

#### 運行測試
```bash
# 使用 pytest
uv run pytest tests/ -v

# 測試覆蓋率
uv run pytest tests/ --cov=. --cov-report=html

# 單個測試
uv run pytest tests/test_modbus_monitor.py::test_connect_success
```

## 🤝 貢獻指南

### 提交流程

1. **Fork 專案**
```bash
git clone https://github.com/your-username/modbus_test.git
cd modbus_test
```

2. **創建功能分支**
```bash
git checkout -b feature/add-coil-write-support
```

3. **進行開發**
```bash
# 使用 UV 安裝依賴
uv sync

# 進行修改 (遵循開發指導原則)
# ... 編輯文件 ...

# 運行測試
uv run pytest tests/
```

4. **提交更改**
```bash
git add .
git commit -m "feat: Add write_coil() and write_coils() methods

- Implement single coil write (FC05)  
- Implement multiple coils write (FC15)
- Add unit tests for coil operations
- Update documentation

Refs #123"
```

5. **推送並創建 PR**
```bash
git push origin feature/add-coil-write-support
# 在 GitHub 上創建 Pull Request
```

### Commit Message 規範

使用 [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**類型 (type)**:
- `feat`: 新功能
- `fix`: Bug 修復
- `docs`: 文檔更新
- `style`: 代碼格式調整
- `refactor`: 重構
- `test`: 測試相關
- `chore`: 構建/工具相關

**範例**:
```
feat(backend): Add WebSocket support for real-time data

Implement WebSocket endpoint /ws for streaming Modbus data
to connected clients without polling.

- Add WebSocket route in main.py
- Implement broadcast mechanism  
- Add connection management
- Update frontend to use WebSocket

Closes #456
```

### 代碼審查清單

- [ ] 代碼遵循 PEP 8 規範
- [ ] 添加了適當的類型提示
- [ ] 編寫了 Docstring 文檔
- [ ] 通過所有單元測試
- [ ] 更新了相關文檔
- [ ] 保留了原始代碼註釋 (如有修改)
- [ ] 沒有包含敏感信息 (.env 文件等)

## 📄 許可證

本專案遵循 MIT License。詳見 [LICENSE](LICENSE) 文件。

## 📞 聯繫方式

- **Issue Tracker**: [GitHub Issues](https://github.com/your-repo/modbus_test/issues)
- **Discussion**: [GitHub Discussions](https://github.com/your-repo/modbus_test/discussions)
- **Email**: your.email@example.com

## 🙏 致謝

### 開源專案
- [pymodbus](https://github.com/pymodbus-dev/pymodbus) - 強大的 Modbus 協議實現
- [FastAPI](https://github.com/tiangolo/fastapi) - 現代化 Python Web 框架
- [Vue.js](https://github.com/vuejs/core) - 漸進式 JavaScript 框架
- [Redis](https://github.com/redis/redis) - 高性能內存數據庫
- [UV](https://github.com/astral-sh/uv) - 極速 Python 套件管理器

### 參考資料
- [Modbus Organization](https://modbus.org/) - 官方協議規範
- [Python Asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Glass-morphism Design](https://hype4.academy/tools/glassmorphism-generator)

---

**最後更新**: 2025-11-07  
**專案版本**: 0.1.0  
**Python 版本**: >= 3.10  
**維護狀態**: 🟢 Active Development

**注意**: 在生產環境中使用前,請確保正確配置網絡安全設置、訪問控制和審計日誌。
