# Modbus Holding Register Monitor - Hex to Decimal Converter

## Overview
This tool monitors Modbus TCP holding registers and displays values in both hexadecimal and decimal formats.

## Quick Start

### 1. Configure Your Settings

The tool now supports configuration files! Choose one of the following methods:

#### Method A: Using `.env` file (Recommended)

1. **Install python-dotenv** (if not already installed):
   ```bash
   uv pip install python-dotenv
   ```

2. **Create your configuration file**:
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` file** with your settings:
   ```bash
   MODBUS_HOST=192.168.30.24
   MODBUS_PORT=502
   MODBUS_DEVICE_ID=1
   START_ADDRESS=1
   END_ADDRESS=26
   ```

#### Method B: Using `config.conf` file

1. **Create your configuration file**:
   ```bash
   cp config.conf.example config.conf
   ```

2. **Edit `config.conf` file** with your settings:
   ```ini
   [modbus]
   host = 192.168.30.24
   port = 502
   device_id = 1

   [registers]
   start_address = 1
   end_address = 26
   ```

#### Method C: Using hardcoded values (Legacy)

Edit `example_config.py` directly (not recommended, but still supported):

```python
# Set your Modbus device IP address
host='192.168.30.24',      # Change this to your device IP

# Define the register range to monitor
START_ADDRESS = 1          # Starting address (decimal)
END_ADDRESS = 26           # Ending address (decimal)
```

### 2. Run the Monitor

#### Read-Only Mode (Default)

```bash
uv run python3 example_config.py
```

The application will automatically detect and load configuration from `.env` or `config.conf` files.

#### Write Mode - Command Line

Write values to holding registers directly from command line:

```bash
# Write single register (decimal)
uv run python3 example_config.py --write --address 10 --values 1234

# Write multiple registers (decimal)
uv run python3 example_config.py --write --address 10 --values 100,200,300

# Write multiple registers (hexadecimal - use 0x prefix)
uv run python3 example_config.py --write --address 10 --values 0x64,0xC8,0x12C

# Write then continue monitoring
uv run python3 example_config.py --write --address 10 --values 1234 --monitor
```

#### Write Mode - Interactive

For a user-friendly interactive interface:

```bash
uv run python3 example_config.py --write-interactive
```

Interactive mode will prompt you for:
- Register address (decimal)
- Values to write (comma-separated, supports hex with 0x prefix)
- Write confirmation
- Optional read-back verification

### 3. Output Format

The program will display:

```
================================================================================
📡 MODBUS MONITOR - Holding Registers (HEX to Decimal Converter)
================================================================================
Target Device    : 192.168.30.24:502
Device ID        : 1
Poll Interval    : 2.0s
Register Range   : 1 to 26 (26 registers)
Address Range    : 0x0001 to 0x001A
================================================================================

================================================================================
🔄 Processing 1 readings...
================================================================================

📊 Holding_Registers_1-26:
   Start Address: 1 (0x0001)
   Count: 26 registers

   Address      Hex Value    Decimal Value
   ----------------------------------------
   1            0x3C3A       15418
   2            0x3C3A       15418
   3            0x3C3A       15418
   ...

   Statistics:
   - Average: 15418.00 (0x3C3A)
   - Maximum: 15418 (0x3C3A)
   - Minimum: 15418 (0x3C3A)
```

## Write Holding Registers

The tool now supports writing values to Modbus holding registers with multiple modes.

### Command-Line Write Mode

Write values directly from command line arguments:

**Write Single Register:**
```bash
uv run python3 example_config.py --write --address 10 --values 1234
```

**Write Multiple Consecutive Registers:**
```bash
# Using decimal values
uv run python3 example_config.py --write --address 10 --values 100,200,300

# Using hexadecimal values (with 0x prefix)
uv run python3 example_config.py --write --address 10 --values 0x64,0xC8,0x12C
```

**Write and Continue Monitoring:**
```bash
uv run python3 example_config.py --write --address 10 --values 1234 --monitor
```

### Interactive Write Mode

For a more user-friendly experience, use the interactive mode:

```bash
uv run python3 example_config.py --write-interactive
```

**Interactive Mode Features:**
- Prompts for register address
- Prompts for values (supports comma-separated for multiple registers)
- Supports both decimal and hexadecimal input (use 0x prefix for hex)
- Displays write operation summary
- Asks for confirmation before writing
- Optional read-back verification
- Can perform multiple write operations in a session
- Type 'q' to quit

**Example Interactive Session:**
```
Enter register address (or 'q' to quit): 10
Enter value(s) (comma-separated for multiple, hex with 0x prefix): 0x1234, 0x5678

📝 Write Operation Summary:
   Address: 10 (0x000A)
   Count: 2 register(s)
   Values: ['4660 (0x1234)', '22136 (0x5678)']

Confirm write? (y/n): y
✅ Write operation completed successfully!

Read back to verify? (y/n): y

✅ Verification Read:
   Address 10 (0x000A): 4660 (0x1234)
   Address 11 (0x000B): 22136 (0x5678)
```

### Command-Line Arguments

| Argument | Description |
|----------|-------------|
| `--write` | Enable command-line write mode (requires `--address` and `--values`) |
| `--write-interactive` | Enable interactive write mode |
| `--address ADDRESS` | Register address to write to (decimal) |
| `--values VALUES` | Comma-separated values (supports decimal or 0x-prefixed hex) |
| `--monitor` | Continue monitoring after write operation |
| `--no-monitor` | Exit after write operation (default behavior) |

### Write Mode Behavior

- **Default after write**: Program exits after successful write
- **With `--monitor`**: Program continues to monitoring mode after write
- **Interactive mode**: After exiting interactive mode, can optionally continue to monitoring with `--monitor`
- **Value range**: All values must be in range 0-65535 (16-bit registers)
- **Address validation**: Addresses should match your Modbus device configuration

### Help and Examples

To see all available options and examples:
```bash
uv run python3 example_config.py --help
```

## Configuration Options

### Configuration File Priority

The application loads configuration in the following order:
1. **`.env` file** (requires `python-dotenv` package)
2. **`config.conf` file** (uses Python's built-in `configparser`)
3. **Hardcoded defaults** (if no config file is found)

### Available Configuration Parameters

| Parameter | `.env` Format | `config.conf` Format | Description | Default |
|-----------|---------------|----------------------|-------------|---------|
| Host | `MODBUS_HOST` | `[modbus] host` | Modbus device IP address | 192.168.30.24 |
| Port | `MODBUS_PORT` | `[modbus] port` | Modbus TCP port | 502 |
| Device ID | `MODBUS_DEVICE_ID` | `[modbus] device_id` | Modbus slave/unit ID | 1 |
| Poll Interval | `MODBUS_POLL_INTERVAL` | `[polling] poll_interval` | Time between reads (seconds) | 2.0 |
| Timeout | `MODBUS_TIMEOUT` | `[polling] timeout` | Connection timeout (seconds) | 3.0 |
| Retries | `MODBUS_RETRIES` | `[polling] retries` | Number of retry attempts | 3 |
| Start Address | `START_ADDRESS` | `[registers] start_address` | First register to read | 1 |
| End Address | `END_ADDRESS` | `[registers] end_address` | Last register to read | 26 |
| Log Level | `LOG_LEVEL` | `[logging] level` | Logging verbosity (DEBUG/INFO/WARNING/ERROR) | INFO |

### Example Configuration Files

#### `.env` Example
```bash
# Modbus TCP Connection Configuration
MODBUS_HOST=192.168.30.24
MODBUS_PORT=502
MODBUS_DEVICE_ID=1

# Polling and Timeout Settings
MODBUS_POLL_INTERVAL=2.0
MODBUS_TIMEOUT=3.0
MODBUS_RETRIES=3

# Register Range Configuration
START_ADDRESS=1
END_ADDRESS=26

# Logging Level
LOG_LEVEL=INFO
```

#### `config.conf` Example
```ini
[modbus]
host = 192.168.30.24
port = 502
device_id = 1

[polling]
poll_interval = 2.0
timeout = 3.0
retries = 3

[registers]
start_address = 1
end_address = 26

[logging]
level = INFO
```

The script automatically calculates the count: `COUNT = END_ADDRESS - START_ADDRESS + 1`

### Multiple Register Ranges

To monitor multiple non-contiguous ranges, add multiple entries:

```python
# Range 1: Registers 1-26
monitor.add_register(
    address=1,
    count=26,
    register_type='holding',
    name='Holding_Registers_1-26'
)

# Range 2: Registers 100-110
monitor.add_register(
    address=100,
    count=11,
    register_type='holding',
    name='Additional_Holding_Regs'
)
```

## Understanding the Output

### Address Display
- **Decimal**: Standard base-10 number (e.g., `1`, `2`, `26`)
- **Hexadecimal**: Base-16 with `0x` prefix (e.g., `0x0001`, `0x001A`)

### Value Display
- **Hex Value**: Raw register value in hexadecimal (e.g., `0x3C3A`)
- **Decimal Value**: Converted to decimal (e.g., `15418`)

Note: `0x3C3A` in hex = `(3×4096) + (12×256) + (3×16) + (10×1)` = `15418` in decimal

### Statistics
- **Average**: Mean of all register values
- **Maximum**: Highest value in the range
- **Minimum**: Lowest value in the range

## Stopping the Monitor

Press `Ctrl+C` to stop monitoring gracefully.

## Troubleshooting

### Connection Issues
- Verify the IP address and port are correct
- Ensure the Modbus device is accessible on the network
- Check firewall settings

### No Data Received
- Verify the device ID (slave ID) is correct
- Check that the register addresses exist on your device
- Try increasing the timeout value

### Example for Different Device

If your Modbus simulator shows:
- Address range: 0x0001 to 0x0010 (1 to 16 in decimal)
- IP: 192.168.1.100

Update the configuration:
```python
host='192.168.1.100',
START_ADDRESS = 1
END_ADDRESS = 16
```

## Related Files
- `async_modbus_monitor.py` - Core monitoring library with read/write functions
- `example_config.py` - Configuration and execution script with write support (this is what you run)
- `.env.example` - Template for `.env` configuration file
- `config.conf.example` - Template for `config.conf` configuration file
- `requirements.txt` - Python package dependencies
- `USAGE.md` - This usage guide with read/write examples

## Installation

Install required dependencies using `uv`:

```bash
# Install all dependencies
uv pip install -r requirements.txt

# Or install individually
uv pip install pymodbus python-dotenv
```
