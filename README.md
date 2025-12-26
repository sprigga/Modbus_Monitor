# Async Modbus Monitor

An asynchronous Modbus data monitoring system based on Python asyncio, providing a CLI tool, a FastAPI backend service, and a Vue 3 frontend interface, with full support for Modbus TCP read/write operations.

## 📋 Project Overview

This project is a comprehensive full-stack Modbus monitoring solution, including:
- **Core Python Module**: Asynchronous Modbus client library with advanced features
- **CLI Tool**: Command-line monitoring and read/write utility with multiple modes
- **REST API Backend**: FastAPI server providing an HTTP interface for programmatic access
- **Modern Web Frontend**: Vue 3 single-page application with glass-morphism design
- **Data Storage**: Redis for time-series data persistence and caching
- **Containerized Deployment**: One-click deployment with Docker Compose
- **Multi-Interface Support**: Seamlessly switch between CLI, API, and Web interfaces

## 🖼️ System Screenshots

Below are screenshots of the main system interface, showcasing the full functionality of the web frontend:

### 1. Web Frontend - Configuration and Connection Control Interface
![Web Frontend Configuration](screenshot/image1.png)
*A modern Vue 3 interface with a glass-morphism design. It includes a complete Modbus configuration panel (Host, Port, Device ID, Poll Interval, address range) and connection control buttons (Update Config, Connect, Disconnect, Start/Stop Monitoring). The top-right corner displays the real-time connection status.*

### 2. Web Frontend - Manual Read Interface
![Web Frontend Manual Read](screenshot/image2.png)
*The Manual Read section allows specifying the register address, count, and register type (Holding/Input/Coils/Discrete Inputs). Below is the area for writing to Holding Registers, supporting single or multiple values (comma-separated). A success notification on the right shows the values read back.*

### 3. Web Frontend - Write Test and Data Monitoring Interface
![Web Frontend Write and Monitor](screenshot/image3.png)
*This demonstrates the complete write and monitoring workflow. The top section is for writing to Holding Registers, with buttons for single and multiple writes. The Modbus Data table below displays real-time monitoring data, including register name, address, type, values, and timestamp. The green notification on the right shows the results of multiple successful reads.*

### 4. API Documentation Interface
Visit `http://localhost:8000/docs` in your browser to see the complete Swagger UI interactive API documentation, allowing developers to quickly test all endpoints (connection, read, write, monitoring, data query, etc.).

## 📁 Project Structure Analysis

### Core File Overview

```
modbus_monitor/
├── async_modbus_monitor.py      (377 lines) - Core asynchronous Modbus client library
├── example_config.py             (492 lines) - CLI tool with configuration and interactive modes
├── start_backend.py             (28 lines)  - Backend service startup script
├── backend/
│   ├── main.py                  (332 lines) - FastAPI REST API application
│   └── modbus_service.py        (297 lines) - Modbus service with Redis integration
├── frontend/
│   ├── index.html               (518 lines) - Vue 3 single-page application
│   ├── app.js                   - Frontend application logic
│   └── css/styles.css           - Modern glass-morphism UI styling
├── docker-compose.yml           - Three-container orchestration (Redis + Backend + Frontend)
├── Dockerfile.backend           - Backend container image definition
├── pyproject.toml               - UV project configuration and dependencies
├── requirements.txt             - Python dependency packages
├── .env.example                 - Environment variable configuration template
├── docs/
│   ├── CLAUDE.md                - Development guidelines and coding standards
│   ├── USAGE.md                 - Detailed usage instructions
│   ├── UML.md                   - System architecture diagrams
│   ├── GITHUB_KEY.md            - GitHub SSH key setup guide
│   └── REFACTOR_SUMMARY.md      - Project refactoring documentation
└── REFACTOR_SUMMARY.md         - Overall project refactoring summary
```

**Total Code**: Approx. 1,522 lines of Python code

### File Function Descriptions

#### Core Modules
- **async_modbus_monitor.py**: A standalone asynchronous Modbus client library that can be used independently or as a base for other modules.
- **example_config.py**: A CLI tool supporting read, write, and monitor modes, loading configuration from `.env` or `config.conf`.

#### Backend Services
- **backend/main.py**: The main FastAPI application, providing RESTful API endpoints.
- **backend/modbus_service.py**: Extends the core Monitor class, integrating Redis for data storage.
- **start_backend.py**: Backend service startup script using uvicorn.

#### Frontend Application
- **frontend/index.html**: A Vue 3 single-page application with a glass-morphism design.
- **frontend/app.js**: Vue application logic, handling API communication and state management.
- **frontend/css/styles.css**: Responsive CSS with modern gradient effects.

#### Configuration & Deployment
- **pyproject.toml**: UV project configuration, defining dependencies and build settings.
- **docker-compose.yml**: Three-container architecture (Redis + Backend + Frontend).
- **Dockerfile.backend**: FastAPI service container image definition.

## 🏗️ System Architecture

### Three-Tier Architecture Design

```
┌─────────────────────────────────────────────────────────┐
│                  Web Frontend (Vue 3)                    │
│              Modern Glass-Morphism UI                    │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST API
┌────────────────────▼────────────────────────────────────┐
│              FastAPI Backend Service                     │
│          (Async HTTP Server + WebSocket Support)        │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │                         │
┌───────▼────────┐     ┌─────────▼──────────┐
│  Modbus Service│     │   Redis Database    │
│  (Async TCP)    │     │  (Time-Series Data) │
└───────┬────────┘     └────────────────────┘
        │
┌───────▼────────────────────────┐
│    Modbus TCP Devices           │
│  (PLC, Sensors, Controllers)    │
└────────────────────────────────┘
```

### Key Architecture Features

1. **Asynchronous Design**: Built on Python asyncio for high performance
2. **Separation of Concerns**: Clean separation between frontend, backend, and data layers
3. **Data Persistence**: Redis integration for caching and historical data
4. **Modular Components**: Each component can be developed and deployed independently
5. **Scalability**: Container-based architecture supports horizontal scaling

### Core Class Structure

#### 1. ModbusConfig - Modbus Connection Configuration
Location: `async_modbus_monitor.py:18-25`

```python
@dataclass
class ModbusConfig:
    host: str                    # Modbus device IP address
    port: int = 502             # Port number (default 502)
    device_id: int = 1          # Device ID (slave ID)
    poll_interval: float = 1.0  # Polling interval (seconds)
    timeout: float = 3.0        # Timeout (seconds)
    retries: int = 3            # Number of retries
```

#### 2. RegisterConfig - Register Configuration
Location: `async_modbus_monitor.py:28-34`

```python
@dataclass
class RegisterConfig:
    address: int                           # Register address
    count: int = 1                        # Number of registers to read
    register_type: str = 'holding'        # Register type
    name: str = None                      # Register name
```

#### 3. AsyncModbusMonitor - Core Monitoring Class
Location: `async_modbus_monitor.py:37-298` (377 lines)

**Main Functional Modules**:

| Category | Method | Lines | Description |
|---|---|---|---|
| Connection | `connect()` | 58-79 | Establish Modbus TCP connection |
| | `disconnect()` | 81-85 | Disconnect and clean up resources |
| Read Ops | `read_register()` | 87-146 | Read a single register configuration |
| | `read_all_registers()` | 148-160 | Concurrently read all configured registers |
| Write Ops | `write_holding_register()` | 162-196 | Write a single holding register (FC06) |
| | `write_holding_registers()` | 198-234 | Write multiple holding registers (FC16) |
| Monitoring | `monitor_continuously()` | 236-286 | Continuous monitoring loop |
| | `add_register()` | 47-56 | Add a register to the monitoring list |
| Utility | `log_data()` | 288-294 | Data logging output |
| | `stop()` | 296-298 | Stop monitoring |

**Key Technical Implementations**:
- Asynchronous communication using `AsyncModbusTcpClient`.
- Concurrent register reading with `asyncio.gather()`.
- Automatic reconnection mechanism (max 5 consecutive errors).
- Support for 4 register types (Holding, Input, Coils, Discrete Inputs).

#### 4. ModbusService - Backend Service Class
Location: `backend/modbus_service.py:39-297` (297 lines)

**Extended Functionality**:

| Feature | Method | Description |
|---|---|---|
| Redis Integration | `store_data_to_redis()` | Store latest data and history |
| Connection Status | `is_connected()` | Check connection status |
| Monitoring Service | `start_monitoring()` | Monitoring loop with Redis storage |
| Formatted Read | `read_registers()` | Return data in REST API format |

**Redis Data Structure**:
- `modbus:latest` - String, stores the latest data as JSON.
- `modbus:history` - Sorted Set, timestamp as score, keeps the last 1000 entries.

## 🎯 Technical Features Analysis

### Asynchronous Architecture
- **Event Loop**: Built on Python `asyncio` for high concurrency
- **Non-blocking I/O**: All network operations use `async/await` pattern
- **Concurrency**: Multiple registers read simultaneously using `asyncio.gather()`
- **Performance Advantage**: Single thread handles hundreds of concurrent connections
- **Automatic Reconnection**: Built-in retry logic with configurable limits

### Comprehensive Write Operations

The system provides robust write operations for Modbus holding registers:

| Operation | Function | Purpose |
|---|---|---|
| Single Write | `write_holding_register()` | Write a single value to one register (Function Code 06) |
| Multiple Write | `write_holding_registers()` | Write multiple values to consecutive registers (Function Code 16) |
| Write Verification | Read-back after write | Verify written values match expected values |
| Hex/Decimal Support | Value parsing | Support for both hexadecimal (0x prefix) and decimal values |
| Error Handling | Exception management | Graceful handling of communication errors

#### Write Operation Implementation (`async_modbus_monitor.py:162-234`)
```python
async def write_holding_register(self, address: int, value: int) -> bool:
    """
    Write a single holding register (FC06)
    Args:
        address: Register address to write to
        value: Value to write (0-65535 for single register)
    Returns:
        True if write successful, False otherwise
    """
    if not self.client or not self.client.connected:
        self.logger.error("Not connected to Modbus device")
        return False

    try:
        result = await self.client.write_register(
            address=address,
            value=value,
            device_id=self.config.device_id
        )

        if not result.isError():
            self.logger.info(f"Successfully wrote value {value} (0x{value:04X}) to address {address} (0x{address:04X})")
            return True
        else:
            self.logger.error(f"Error writing to address {address}: {result}")
            return False
    except ModbusException as exc:
        self.logger.error(f"Modbus exception writing to address {address}: {exc}")
        return False
```

### Error Handling and Fault Tolerance

#### Connection Level (`async_modbus_monitor.py:236-286`)
```python
consecutive_errors = 0
max_consecutive_errors = 5

while self.running:
    if not self.client.connected:
        if not await self.connect():
            consecutive_errors += 1
            if consecutive_errors >= max_consecutive_errors:
                break  # Stop if the limit is exceeded
```

#### Read Level
- Catches `ModbusException`.
- Catches generic `Exception`.
- Detailed error logging.
- Returns `None` instead of raising an exception.

### Data Processing Capabilities

#### CLI Mode (`example_config.py:129-173`)
```python
async def data_processor(data):
    """Supports hexadecimal and decimal display"""
    for item in data:
        # Display address, hex, and decimal value for each register
        for i, value in enumerate(values):
            current_addr = address + i
            print(f"{current_addr:<12} 0x{value:04X}      {value:<15}")

        # Statistical calculations
        avg = sum(values) / len(values)
        max_val = max(values)
        min_val = min(values)
```

#### API Mode (`backend/main.py`)
- Pydantic model validation.
- JSON serialization for output.
- Timestamp normalization (ISO 8601).

### Web Frontend Features

#### Vue 3 Responsive Design (`frontend/index.html`)
```javascript
// Composition API style
data() {
    return {
        config: {...},      # Configuration state
        status: {...},      # Connection state
        latestData: null,   # Latest data
        autoRefresh: false  # Auto-refresh switch
    }
}
```

#### Glass-Morphism UI (`frontend/css/styles.css`)
```css
.glass-card {
    background: var(--background-glass);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-color);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
```

## 🚀 Features

### 1. Complete Modbus Operations

#### Supported Register Types

| Type | Modbus Function Code | Read | Write | Data Type | Typical Use |
|---|---|---|---|---|---|
| Holding Registers | FC03, FC06, FC16 | ✅ | ✅ | 16-bit | Setpoints, parameters |
| Input Registers | FC04 | ✅ | ❌ | 16-bit | Sensor readings |
| Coils | FC01, FC05, FC15 | ✅ | ✅ | 1-bit | Digital output control |
| Discrete Inputs | FC02 | ✅ | ❌ | 1-bit | Switch status, alarms |

**Note**: Write operations are fully implemented for Holding Registers (FC06, FC16). Coil write operations (FC05, FC15) are supported in the backend service and can be extended to frontend/CLI as needed.

#### Read Operation Implementation (`async_modbus_monitor.py:87-146`)
```python
async def read_register(self, reg_config: RegisterConfig):
    if reg_config.register_type == 'holding':
        result = await self.client.read_holding_registers(
            reg_config.address,
            count=reg_config.count,
            device_id=self.config.device_id
        )
    # ... other types implemented similarly
```

### 2. Three Usage Modes

#### A. CLI Mode

**Basic Usage** (`example_config.py:302-492`):

```bash
# 1. Read-only monitoring mode
uv run python example_config.py

# 2. Write a single register
uv run python example_config.py --write --address 10 --values 1234

# 3. Write multiple registers (decimal)
uv run python example_config.py --write --address 10 --values 100,200,300

# 4. Write multiple registers (hexadecimal)
uv run python example_config.py --write --address 10 --values 0x64,0xC8,0x12C

# 5. Interactive write mode
uv run python example_config.py --write-interactive

# 6. Monitor after writing
uv run python example_config.py --write --address 10 --values 1234 --monitor
```

**Interactive Write Feature** (`example_config.py:175-277`):
```
Enter register address (or 'q' to quit): 10
Enter value(s) (comma-separated, hex with 0x): 0x3C,0x64
Confirm write? (y/n): y
✅ Write operation completed!
Read back to verify? (y/n): y
```

**Command-Line Arguments**:

| Argument | Description |
|---|---|
| `--write` | Enable command-line write mode (requires `--address` and `--values`) |
| `--write-interactive` | Enable interactive write mode |
| `--address ADDRESS` | Register address to write to (decimal) |
| `--values VALUES` | Comma-separated values to write (supports hex with 0x prefix) |
| `--monitor` | Continue monitoring after write operation |
| `--no-monitor` | Exit after write operation (default behavior when write is completed) |

#### B. REST API Mode

**Start the backend service**:
```bash
# Method 1: Using start_backend.py
uv run python start_backend.py

# Method 2: Directly with uvicorn
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**API Endpoint List** (`backend/main.py:64-330`):

| Endpoint | Method | Function | Request Body |
|---|---|---|---|
| `/api/config` | GET | Get configuration | - |
| `/api/config` | POST | Update configuration | ModbusConfigModel |
| `/api/connect` | POST | Connect to device | - |
| `/api/disconnect` | POST | Disconnect from device | - |
| `/api/status` | GET | Get status | - |
| `/api/read` | POST | Read registers | RegisterReadRequest |
| `/api/write` | POST | Write a single register | RegisterWriteRequest |
| `/api/write_multiple` | POST | Write multiple registers | MultipleRegisterWriteRequest |
| `/api/start_monitoring` | POST | Start monitoring | - |
| `/api/stop_monitoring` | POST | Stop monitoring | - |
| `/api/data/latest` | GET | Get latest data | - |
| `/api/data/history` | GET | Get historical data | `limit` (query param) |

**API Usage Example**:
```bash
# Connect to device
curl -X POST http://localhost:8000/api/connect

# Read registers
curl -X POST http://localhost:8000/api/read \
  -H "Content-Type: application/json" \
  -d '{"address": 0, "count": 10, "register_type": "holding"}'

# Write a register
curl -X POST http://localhost:8000/api/write \
  -H "Content-Type: application/json" \
  -d '{"address": 10, "value": 1234}'

# Write multiple registers
curl -X POST http://localhost:8000/api/write_multiple \
  -H "Content-Type: application/json" \
  -d '{"address": 10, "values": [100, 200, 300]}'

# Get latest data
curl http://localhost:8000/api/data/latest

# Get historical data (last 50 entries)
curl "http://localhost:8000/api/data/history?limit=50"
```

#### C. Web Interface Mode

**Access**: `http://localhost:8081`

**Interface Features** (`frontend/index.html`):
1.  **Configuration Panel**: Dynamically modify Modbus connection parameters.
2.  **Connection Control**: Connect/Disconnect/Start Monitoring/Stop buttons.
3.  **Manual Read**: Read by specifying address, count, and register type.
4.  **Write Operations**: Write single or multiple registers to holding registers with immediate feedback.
5.  **Write Single Register**: Specify address and value to write a single 16-bit register.
6.  **Write Multiple Registers**: Write multiple consecutive registers using comma-separated values.
7.  **Data Display**: Real-time data shown in a table with timestamp and value verification.
8.  **Auto-Refresh**: Toggle automatic data updates.
9.  **Status Indicators**: Visual indicators for connection and monitoring status.

### 3. Flexible Configuration Management

#### Configuration Priority (`example_config.py:92-127`)

```python
def load_config():
    """
    Configuration source priority:
    1. .env file (highest)
    2. config.conf file
    3. Hardcoded defaults (lowest)
    """
    config = load_config_from_env()
    if config: return config

    config = load_config_from_conf()
    if config: return config

    return default_config  # Hardcoded defaults
```

#### .env File Format (`.env.example`)
```bash
# Modbus device network configuration
MODBUS_HOST=192.168.30.24
MODBUS_PORT=502
MODBUS_DEVICE_ID=1

# Polling and timeout settings
MODBUS_POLL_INTERVAL=2.0
MODBUS_TIMEOUT=3.0
MODBUS_RETRIES=3

# Register range configuration (for monitoring)
START_ADDRESS=1
END_ADDRESS=26

# Log level
LOG_LEVEL=INFO
```

#### config.conf File Format (Alternative Configuration)
```ini
[modbus]
# Modbus TCP Connection Configuration
host = 192.168.30.24
port = 502
device_id = 1

[polling]
# Polling and Timeout Settings
poll_interval = 2.0
timeout = 3.0
retries = 3

[registers]
# Register Range Configuration
start_address = 1
end_address = 26

[logging]
# Logging Level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
level = INFO

# Optional: Additional Register Ranges
# Uncomment and configure as needed
# [input_registers]
# start = 100
# count = 8

# [coils]
# start = 0
# count = 16

# [discrete_inputs]
# start = 100
# count = 8
```

The configuration system supports both `.env` and `.conf` files with priority given to `.env` if both exist.

## 📦 Dependency Analysis

### Python Dependencies (`pyproject.toml`)

#### Core Dependencies
```toml
[project.dependencies]
pymodbus = ">=3.0.0"        # Modbus protocol implementation, ~50KB
python-dotenv = ">=1.0.0"   # Environment variable management, ~20KB
```

#### Backend-Specific Dependencies
```toml
fastapi = ">=0.104.0"             # Web framework, ~300KB
uvicorn[standard] = ">=0.24.0"    # ASGI server, ~200KB
redis = ">=5.0.0"                 # Redis client, ~150KB
pydantic = ">=2.0.0"              # Data validation, ~400KB
python-multipart = ">=0.0.6"      # Form handling, ~30KB
```

#### Standard Library (No installation required)
```python
import asyncio       # Asynchronous I/O
import logging       # Logging
import datetime      # Time handling
import json          # JSON serialization
import typing        # Type hints
import dataclasses   # Data classes
import configparser  # INI config parsing
import argparse      # Command-line argument parsing
```

### System Dependencies

- **Python**: >= 3.10 (uses `match-case` and modern type hints)
- **Redis**: >= 7.0 (for time-series data storage)
- **UV**: Python package manager (recommended, 10-100x faster than pip)
- **Docker**: >= 20.10 (optional, for containerized deployment)

### Frontend Dependencies (Loaded via CDN)

```html
<!-- Vue 3 Framework -->
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>

<!-- Axios HTTP Client -->
<script src="https://unpkg.com/axios/dist/axios.min.js"></script>

<!-- Font Awesome Icons -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
```

## 🔧 Installation and Setup

### Prerequisites

- **Python**: >= 3.10 (uses `match-case` and modern type hints)
- **Redis**: >= 7.0 (for data storage)
- **UV**: Python package manager (recommended, 10-100x faster than pip)
- **Docker**: >= 20.10 (optional, for containerized deployment)

### Method 1: Using UV (Recommended)

```bash
# 1. Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone the project
git clone <repository-url>
cd modbus_monitor

# 3. Sync dependencies with UV
uv sync

# 4. Configure environment variables
cp .env.example .env
nano .env  # Edit configuration

# 5. Start Redis (if using the backend)
docker run -d -p 6379:6379 --name modbus-redis redis:7-alpine

# 6. Run the CLI tool
uv run python example_config.py

# 7. Start the backend service (optional)
uv run python start_backend.py
```

### Method 2: Using Docker Compose

```bash
# 1. Configure environment variables
cp .env.example .env
nano .env  # Modify MODBUS_HOST, etc.

# 2. Start all services (one-click deployment)
docker-compose up -d

# 3. Check service status
docker-compose ps

# 4. View logs
docker-compose logs -f backend

# 5. Access services
# - Web Frontend: http://localhost:8081
# - API Docs: http://localhost:8000/docs
# - Redis: localhost:6380

# 6. Stop services
docker-compose down
```

### Method 3: Traditional Pip Installation

```bash
# 1. Create a virtual environment
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure the environment
cp .env.example .env

# 6. Run the program
python example_config.py
```

## 💡 Usage Examples

### Example 1: Basic Read Monitoring

File: `examples/basic_read.py`

```python
from async_modbus_monitor import AsyncModbusMonitor, ModbusConfig
import asyncio
import logging

async def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Configure connection
    config = ModbusConfig(
        host='192.168.1.100',
        port=502,
        device_id=1,
        poll_interval=2.0,
        timeout=5.0
    )

    # Create monitor
    monitor = AsyncModbusMonitor(config)

    # Add registers to monitor
    monitor.add_register(
        address=0,           # Start address
        count=10,           # Read 10 registers
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
        # Connect to device
        if await monitor.connect():
            print("✅ Connection successful!")

            # Start continuous monitoring
            await monitor.monitor_continuously()
    except KeyboardInterrupt:
        print("\n⏹️  Stopping monitoring...")
        monitor.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 2: Writing Registers

File: `examples/write_registers.py`

```python
from async_modbus_monitor import AsyncModbusMonitor, ModbusConfig, RegisterConfig
import asyncio

async def write_example():
    config = ModbusConfig(host='192.168.1.100')
    monitor = AsyncModbusMonitor(config)

    if await monitor.connect():
        print("Connected to Modbus device")

        # Write a single register
        success = await monitor.write_holding_register(
            address=10,
            value=1234
        )
        print(f"Single register write: {'Success' if success else 'Failed'}")

        # Write multiple registers
        success = await monitor.write_holding_registers(
            address=20,
            values=[100, 200, 300, 400, 500]
        )
        print(f"Multiple registers write: {'Success' if success else 'Failed'}")

        # Read back for verification
        reg_config = RegisterConfig(
            address=10,
            count=1,
            register_type='holding'
        )
        result = await monitor.read_register(reg_config)
        if result:
            print(f"Verification read: Address 10 = {result['values'][0]}")

        await monitor.disconnect()

asyncio.run(write_example())
```

### Example 3: Custom Data Processing

File: `examples/custom_processor.py`

```python
from async_modbus_monitor import AsyncModbusMonitor, ModbusConfig
import asyncio
from typing import List, Dict, Any

async def temperature_processor(data: List[Dict[str, Any]]):
    """Temperature data processor - converts to Celsius"""
    print(f"\n{'='*60}")
    print(f"📊 Temperature Monitoring Report - {len(data)} readings")
    print(f"{'='*60}")

    for item in data:
        name = item['name']
        raw_values = item['values']

        # Assume raw value needs to be divided by 10 for actual temperature
        temperatures = [v / 10.0 for v in raw_values]

        # Statistical analysis
        avg_temp = sum(temperatures) / len(temperatures)
        max_temp = max(temperatures)
        min_temp = min(temperatures)

        print(f"\n🌡️  {name}:")
        print(f"   Temperature range: {temperatures}")
        print(f"   Average temperature: {avg_temp:.1f}°C")
        print(f"   Maximum temperature: {max_temp:.1f}°C")
        print(f"   Minimum temperature: {min_temp:.1f}°C")

        # Alarm check
        if max_temp > 80.0:
            print(f"   ⚠️  Warning: Temperature too high!")
        elif max_temp > 70.0:
            print(f"   ⚡ Notice: Temperature is high")

async def main():
    config = ModbusConfig(
        host='192.168.1.100',
        poll_interval=5.0  # Update every 5 seconds
    )

    monitor = AsyncModbusMonitor(config)
    monitor.add_register(0, 8, 'input', 'Furnace_Sensors')
    monitor.add_register(100, 4, 'input', 'Ambient_Temperature')

    if await monitor.connect():
        # Use the custom processor
        await monitor.monitor_continuously(
            data_callback=temperature_processor
        )

asyncio.run(main())
```

### Example 4: Multi-Device Monitoring

File: `examples/multi_device.py`

```python
import asyncio
from async_modbus_monitor import AsyncModbusMonitor, ModbusConfig

async def monitor_device(device_name: str, host: str):
    """Monitor a single device"""
    config = ModbusConfig(host=host, poll_interval=2.0)
    monitor = AsyncModbusMonitor(config)

    monitor.add_register(0, 10, 'holding', f'{device_name}_Holdings')

    if await monitor.connect():
        print(f"✅ {device_name} connected")

        async def device_callback(data):
            for item in data:
                print(f"[{device_name}] {item['name']}: {item['values']}")

        await monitor.monitor_continuously(data_callback=device_callback)

async def main():
    """Concurrently monitor multiple devices"""
    devices = [
        ("PLC-1", "192.168.1.100"),
        ("PLC-2", "192.168.1.101"),
        ("PLC-3", "192.168.1.102"),
    ]

    # Concurrently execute multiple monitoring tasks
    tasks = [monitor_device(name, host) for name, host in devices]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔐 Security Considerations

### Production Deployment Checklist

#### 1. Network Security
- [ ] Use a firewall to restrict access to the Modbus port (502).
- [ ] Isolate Modbus devices on a dedicated VLAN.
- [ ] Use a VPN for remote access.
- [ ] Disable unnecessary services and ports.

#### 2. API Security (requires modification in `backend/main.py`)

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """JWT Token validation"""
    token = credentials.credentials
    # Implement token validation logic
    if not validate_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# Protected endpoint
@app.post("/api/write", dependencies=[Depends(verify_token)])
async def write_register(...):
    pass
```

#### 3. CORS Configuration

```python
# Restrict allowed origins in a production environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-domain.com",
        "https://app.your-domain.com"
    ],  # Replace with your actual domain
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Restrict allowed methods
    allow_headers=["Authorization", "Content-Type"],
)
```

#### 4. Environment Variable Management

```bash
# Do not commit sensitive information to version control
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore

# Use a secret management service
# AWS: Secrets Manager
# Azure: Key Vault
# GCP: Secret Manager
```

#### 5. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/write")
@limiter.limit("10/minute")  # Max 10 writes per minute
async def write_register(...):
    pass
```

#### 6. Audit Logging

```python
import logging
from datetime import datetime

# Log all write operations
async def log_write_operation(user: str, address: int, value: int):
    logging.info(
        f"WRITE_AUDIT: user={user}, address={address}, "
        f"value={value}, timestamp={datetime.now().isoformat()}"
    )

@app.post("/api/write")
async def write_register(request: RegisterWriteRequest, user=Depends(get_current_user)):
    await log_write_operation(user.username, request.address, request.value)
    # ... execute write
```

#### 7. HTTPS Configuration

```bash
# Obtain a free SSL certificate using Let's Encrypt
certbot certonly --standalone -d your-domain.com

# Nginx reverse proxy configuration
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

#### 8. Authentication and Authorization

```python
# Multi-factor authentication setup
# - Implement OAuth2 for third-party integrations
# - Set up role-based access control (RBAC)
# - Use API keys for device-to-device communication
# - Implement session management with proper timeout

# Security headers
app.add_middleware(
    SecurityHeadersMiddleware,
    content_security_policy="default-src 'self'",
    strict_transport_security="max-age=31536000; includeSubDomains",
)
```

## 🔧 Troubleshooting

### Issue 1: Connection Failed

**Error Message**:
```
Failed to connect to Modbus device
Connection error: [Errno 113] No route to host
```

**Diagnostic Steps**:
```bash
# 1. Test network connectivity
ping 192.168.1.100

# 2. Test port connectivity
nc -zv 192.168.1.100 502

# 3. Check firewall
sudo iptables -L -n | grep 502

# 4. View device logs
uv run python example_config.py 2>&1 | tee modbus.log
```

**Solution**:
- Confirm the IP address is correct.
- Check if the device has Modbus TCP enabled.
- Adjust firewall rules to allow port 502.
- Increase the timeout parameter: `timeout=10.0`.

### Issue 2: Read Error

**Error Message**:
```
Error reading Holding_0-9: Modbus Error: [Input/Output] Modbus Error: [Invalid Message] Incomplete message received, expected at least 8 bytes
```

**Diagnosis**:
```python
# Enable detailed logging
logging.getLogger('pymodbus').setLevel(logging.DEBUG)

# Test with a single register
monitor.add_register(0, 1, 'holding', 'Test_Single')
```

**Solution**:
- Reduce the `count` (some devices limit the number of registers per read).
- Verify the register address exists.
- Check if the `device_id` is correct.
- Confirm the register type (holding vs. input).

### Issue 3: Redis Connection Failed

**Error Message**:
```
redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379. Connection refused.
```

**Solution**:
```bash
# Check if Redis is running
redis-cli ping

# If not running, start Redis
docker run -d -p 6379:6379 redis:7-alpine

# Or use the system service
sudo systemctl start redis
sudo systemctl enable redis

# Check Redis version
redis-cli INFO server | grep redis_version
```

### Issue 4: Performance Issues

**Symptoms**: Slow data updates, high CPU usage.

**Performance Analysis**:
```python
import cProfile
import pstats

# Performance profiling
profiler = cProfile.Profile()
profiler.enable()

await monitor.monitor_continuously()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

**Optimization Suggestions**:
```python
# 1. Increase the polling interval
config = ModbusConfig(poll_interval=5.0)  # From 1.0 to 5.0

# 2. Reduce the number of concurrent reads
monitor.add_register(0, 10, 'holding')  # Change to batch reads
monitor.add_register(10, 10, 'holding')

# 3. Use a connection pool (for multi-device scenarios)
# 4. Enable Redis persistence optimization
```

### Issue 5: Docker Container Problems

**Error**: Container fails to start.

```bash
# View container logs
docker-compose logs backend

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Enter the container for debugging
docker-compose exec backend /bin/bash

# Check the network
docker network inspect modbus_test_default
```

## 📚 API Documentation

### REST API Detailed Description

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### API Request/Response Examples

#### 1. Connect Device

**Request**:
```http
POST /api/connect HTTP/1.1
Content-Type: application/json
```

**Response**:
```json
{
  "message": "Connected successfully"
}
```

#### 2. Read Registers

**Request**:
```http
POST /api/read HTTP/1.1
Content-Type: application/json

{
  "address": 0,
  "count": 10,
  "register_type": "holding"
}
```

**Response**:
```json
{
  "address": 0,
  "type": "holding",
  "count": 10,
  "values": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
  "timestamp": "2025-11-07T10:30:45.123456"
}
```

#### 3. Write Register

**Request**:
```http
POST /api/write HTTP/1.1
Content-Type: application/json

{
  "address": 10,
  "value": 1234
}
```

**Response**:
```json
{
  "message": "Successfully wrote value 1234 to address 10"
}
```

#### 4. Get Latest Data

**Request**:
```http
GET /api/data/latest HTTP/1.1
```

**Response**:
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

## 📝 Development Guidelines

### Code Modification Standards (According to CLAUDE.md)

#### 1. Use UV to Manage the Python Environment
```bash
# ✅ Correct: Use uv run
uv run python script.py
uv run pytest tests/

# ❌ Incorrect: Directly use python
python script.py
```

#### 2. Preserve Original Code with Comments

**Example: Modifying a function**:
```python
# ===== Original Code (COMMENTED OUT - 2025-11-07) =====
# def process_data(data):
#     """Original implementation - synchronous processing"""
#     result = []
#     for item in data:
#         result.append(transform(item))
#     return result

# ===== New Code (UPDATED - 2025-11-07) =====
# Reason for change: Switched to async for better performance
async def process_data(data):
    """Asynchronously process multiple data items"""
    tasks = [transform_async(item) for item in data]
    return await asyncio.gather(*tasks)
```

**Example: Modifying configuration**:
```python
# ===== Original Config (COMMENTED OUT - using config.conf) =====
# config = ModbusConfig(
#     host='192.168.30.24',
#     port=502,
#     device_id=1,
#     poll_interval=2.0
# )

# ===== New Config (UPDATED - loaded from .env) =====
# Reason for change: Support for environment variables for more flexibility
config = ModbusConfig(
    host=os.getenv('MODBUS_HOST', '192.168.30.24'),
    port=int(os.getenv('MODBUS_PORT', 502)),
    device_id=int(os.getenv('MODBUS_DEVICE_ID', 1)),
    poll_interval=float(os.getenv('MODBUS_POLL_INTERVAL', 2.0))
)
```

### Code Style Guide

#### Type Hinting
```python
from typing import List, Dict, Any, Optional

async def read_multiple_registers(
    addresses: List[int],
    counts: List[int],
    register_type: str = 'holding'
) -> List[Optional[Dict[str, Any]]]:
    """Complete type hinting"""
    pass
```

#### Docstring Format
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

### Testing Guide

#### Unit Test Example
```python
# tests/test_modbus_monitor.py
import pytest
from async_modbus_monitor import AsyncModbusMonitor, ModbusConfig

@pytest.mark.asyncio
async def test_connect_success():
    """Test successful connection"""
    config = ModbusConfig(host='localhost', port=5020)
    monitor = AsyncModbusMonitor(config)

    result = await monitor.connect()
    assert result == True
    assert monitor.client.connected == True

    await monitor.disconnect()

@pytest.mark.asyncio  
async def test_read_holding_registers():
    """Test reading Holding Registers"""
    config = ModbusConfig(host='localhost')
    monitor = AsyncModbusMonitor(config)

    await monitor.connect()
    monitor.add_register(0, 10, 'holding', 'Test')

    data = await monitor.read_all_registers()
    assert len(data) == 1
    assert data[0]['name'] == 'Test'
    assert len(data[0]['values']) == 10
```

#### Running Tests
```bash
# Using pytest
uv run pytest tests/ -v

# Test coverage
uv run pytest tests/ --cov=. --cov-report=html

# Single test
uv run pytest tests/test_modbus_monitor.py::test_connect_success
```

## 🤝 Contribution Guide

### Submission Process

1.  **Fork the project**
    ```bash
    git clone https://github.com/your-username/modbus_test.git
    cd modbus_test
    ```

2.  **Create a feature branch**
    ```bash
    git checkout -b feature/add-coil-write-support
    ```

3.  **Develop**
    ```bash
    # Install dependencies with UV
    uv sync

    # Make changes (following development guidelines)
    # ... edit files ...

    # Run tests
    uv run pytest tests/
    ```

4.  **Commit changes**
    ```bash
    git add .
    git commit -m "feat: Add write_coil() and write_coils() methods

    - Implement single coil write (FC05)  
    - Implement multiple coils write (FC15)
    - Add unit tests for coil operations
    - Update documentation

    Refs #123"
    ```

5.  **Push and create a PR**
    ```bash
    git push origin feature/add-coil-write-support
    # Create a Pull Request on GitHub
    ```

### Commit Message Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation update
- `style`: Code style adjustments
- `refactor`: Refactoring
- `test`: Test-related
- `chore`: Build/tool-related

**Example**:
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

### Code Review Checklist

- [ ] Code follows PEP 8 standards.
- [ ] Appropriate type hints have been added.
- [ ] Docstrings have been written.
- [ ] All unit tests pass.
- [ ] Relevant documentation has been updated.
- [ ] Original code comments are preserved (if modified).
- [ ] No sensitive information (.env files, etc.) is included.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Issue Tracker**: [GitHub Issues](https://github.com/your-repo/modbus_test/issues)
- **Discussion**: [GitHub Discussions](https://github.com/your-repo/modbus_test/discussions)
- **Email**: your.email@example.com

## 🙏 Acknowledgements

### Open Source Projects
- [pymodbus](https://github.com/pymodbus-dev/pymodbus) - A powerful Modbus protocol implementation.
- [FastAPI](https://github.com/tiangolo/fastapi) - A modern Python web framework.
- [Vue.js](https://github.com/vuejs/core) - A progressive JavaScript framework.
- [Redis](https://github.com/redis/redis) - A high-performance in-memory database.
- [UV](https://github.com/astral-sh/uv) - An extremely fast Python package manager.

### References
- [Modbus Organization](https://modbus.org/) - Official protocol specifications.
- [Python Asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Glass-morphism Design](https://hype4.academy/tools/glassmorphism-generator)

---

**Last Updated**: 2025-11-07
**Project Version**: 0.1.0
**Python Version**: >= 3.10
**Maintenance Status**: 🟢 Active Development

**Note**: Before using in a production environment, ensure proper configuration of network security settings, access control, and audit logging.