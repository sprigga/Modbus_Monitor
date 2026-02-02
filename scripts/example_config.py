#!/usr/bin/env python3
"""
Example configuration file for async Modbus monitor
Supports loading configuration from .env or .conf files

This script reads Modbus holding registers and converts hex values to decimal.

Usage:
1. Copy .env.example to .env OR config.conf.example to config.conf
2. Modify the configuration file with your Modbus device settings
3. Run: python3 example_config.py

Configuration file priority:
1. .env file (requires python-dotenv: uv pip install python-dotenv)
2. config.conf file (uses built-in configparser)
3. Hardcoded defaults (if no config file found)

The output will show:
- Address of each register (in decimal and hex)
- Value in hexadecimal format (e.g., 0x3C3A)
- Value in decimal format (e.g., 15418)
- Statistics (min, max, average)
"""

from async_modbus_monitor import AsyncModbusMonitor, ModbusConfig, RegisterConfig
import asyncio
import logging
import os
import configparser
import argparse
from pathlib import Path
from typing import List

# Try to import python-dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    logging.warning("python-dotenv not installed. Install with: uv pip install python-dotenv")


def load_config_from_env():
    """Load configuration from .env file"""
    env_path = Path('.env')
    if not env_path.exists():
        return None

    if not DOTENV_AVAILABLE:
        logging.warning(".env file found but python-dotenv is not installed")
        return None

    load_dotenv()
    logging.info("Loading configuration from .env file")

    return {
        'host': os.getenv('MODBUS_HOST', '192.168.30.24'),
        'port': int(os.getenv('MODBUS_PORT', '502')),
        'device_id': int(os.getenv('MODBUS_DEVICE_ID', '1')),
        'poll_interval': float(os.getenv('MODBUS_POLL_INTERVAL', '2.0')),
        'timeout': float(os.getenv('MODBUS_TIMEOUT', '3.0')),
        'retries': int(os.getenv('MODBUS_RETRIES', '3')),
        'start_address': int(os.getenv('START_ADDRESS', '1')),
        'end_address': int(os.getenv('END_ADDRESS', '26')),
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
    }


def load_config_from_conf():
    """Load configuration from config.conf file"""
    conf_path = Path('config.conf')
    if not conf_path.exists():
        return None

    logging.info("Loading configuration from config.conf file")
    config = configparser.ConfigParser()
    config.read(conf_path)

    return {
        'host': config.get('modbus', 'host', fallback='192.168.30.24'),
        'port': config.getint('modbus', 'port', fallback=502),
        'device_id': config.getint('modbus', 'device_id', fallback=1),
        'poll_interval': config.getfloat('polling', 'poll_interval', fallback=2.0),
        'timeout': config.getfloat('polling', 'timeout', fallback=3.0),
        'retries': config.getint('polling', 'retries', fallback=3),
        'start_address': config.getint('registers', 'start_address', fallback=1),
        'end_address': config.getint('registers', 'end_address', fallback=26),
        'log_level': config.get('logging', 'level', fallback='INFO'),
    }


def load_config():
    """
    Load configuration from available sources in order of priority:
    1. .env file
    2. config.conf file
    3. Hardcoded defaults
    """
    # Try .env file first
    config = load_config_from_env()
    if config:
        logging.info("✓ Configuration loaded from .env file")
        return config

    # Try config.conf file
    config = load_config_from_conf()
    if config:
        logging.info("✓ Configuration loaded from config.conf file")
        return config

    # Use hardcoded defaults
    logging.warning("⚠ No configuration file found (.env or config.conf)")
    logging.warning("⚠ Using hardcoded default values")
    logging.info("💡 Copy .env.example to .env or config.conf.example to config.conf to customize")

    return {
        'host': '192.168.30.24',
        'port': 502,
        'device_id': 1,
        'poll_interval': 2.0,
        'timeout': 3.0,
        'retries': 3,
        'start_address': 1,
        'end_address': 26,
        'log_level': 'INFO',
    }


async def data_processor(data):
    """Custom data processing function - Convert hex to decimal"""
    print(f"\n{'='*80}")
    print(f"🔄 Processing {len(data)} readings...")
    print(f"{'='*80}")

    for item in data:
        name = item['name']
        values = item['values']
        address = item['address']

        # Example: Process specific registers
        if 'Holding' in name:
            # Process holding registers - Display in both HEX and Decimal
            print(f"\n📊 {name}:")
            print(f"   Start Address: {address} (0x{address:04X})")
            print(f"   Count: {len(values)} registers")
            print(f"\n   {'Address':<12} {'Hex Value':<12} {'Decimal Value':<15}")
            print(f"   {'-'*40}")

            for i, value in enumerate(values):
                current_addr = address + i
                # Display each register: address, hex value, decimal value
                print(f"   {current_addr:<12} 0x{value:04X}      {value:<15}")

            # Statistics
            avg_value = sum(values) / len(values) if values else 0
            max_value = max(values) if values else 0
            min_value = min(values) if values else 0
            print(f"\n   Statistics:")
            print(f"   - Average: {avg_value:.2f} (0x{int(avg_value):04X})")
            print(f"   - Maximum: {max_value} (0x{max_value:04X})")
            print(f"   - Minimum: {min_value} (0x{min_value:04X})")

        elif 'Input' in name:
            # Process input registers (e.g., sensor readings)
            print(f"\n📊 {name}:")
            print(f"   Decimal values: {values}")
            print(f"   Hex values: {[f'0x{v:04X}' for v in values]}")

        elif 'Coils' in name:
            # Process coils (e.g., digital outputs)
            active_coils = [i for i, v in enumerate(values) if v]
            print(f"\n📊 {name}: Active coils = {active_coils}")


async def write_registers_interactive(monitor: AsyncModbusMonitor):
    """Interactive function to write holding registers"""
    print("\n" + "="*80)
    print("✍️  WRITE HOLDING REGISTERS - Interactive Mode")
    print("="*80)
    print("This mode allows you to write values to holding registers.")
    print("You can write a single value or multiple values to consecutive registers.")
    print("="*80 + "\n")

    while True:
        try:
            # Get starting address
            addr_input = input("Enter register address (or 'q' to quit): ").strip()
            if addr_input.lower() == 'q':
                break

            try:
                address = int(addr_input)
            except ValueError:
                print("❌ Invalid address. Please enter a decimal number.")
                continue

            # Get values to write
            values_input = input("Enter value(s) (comma-separated for multiple, hex with 0x prefix): ").strip()
            if not values_input:
                print("❌ No values provided.")
                continue

            # Parse values
            values_str = [v.strip() for v in values_input.split(',')]
            values = []

            for v_str in values_str:
                try:
                    # Support hex (0x prefix) or decimal
                    if v_str.lower().startswith('0x'):
                        value = int(v_str, 16)
                    else:
                        value = int(v_str)

                    # Validate range for 16-bit register
                    if value < 0 or value > 65535:
                        print(f"❌ Value {value} out of range (0-65535)")
                        values = []
                        break

                    values.append(value)
                except ValueError:
                    print(f"❌ Invalid value: {v_str}")
                    values = []
                    break

            if not values:
                continue

            # Confirm write operation
            print(f"\n📝 Write Operation Summary:")
            print(f"   Address: {address} (0x{address:04X})")
            print(f"   Count: {len(values)} register(s)")
            print(f"   Values: {[f'{v} (0x{v:04X})' for v in values]}")

            confirm = input("\nConfirm write? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ Write operation cancelled.")
                continue

            # Perform write
            if len(values) == 1:
                success = await monitor.write_holding_register(address, values[0])
            else:
                success = await monitor.write_holding_registers(address, values)

            if success:
                print("✅ Write operation completed successfully!")

                # Read back to verify
                verify = input("Read back to verify? (y/n): ").strip().lower()
                if verify == 'y':
                    reg_config = RegisterConfig(
                        address=address,
                        count=len(values),
                        register_type='holding',
                        name=f'Verify_Read_{address}'
                    )
                    result = await monitor.read_register(reg_config)
                    if result:
                        print(f"\n✅ Verification Read:")
                        for i, val in enumerate(result['values']):
                            addr = address + i
                            print(f"   Address {addr} (0x{addr:04X}): {val} (0x{val:04X})")
                    else:
                        print("❌ Failed to read back values")
            else:
                print("❌ Write operation failed!")

            print()

        except KeyboardInterrupt:
            print("\n\n⏹️  Exiting write mode...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


async def write_from_args(monitor: AsyncModbusMonitor, address: int, values: List[int]) -> bool:
    """Write registers from command-line arguments"""
    print("\n" + "="*80)
    print("✍️  WRITE HOLDING REGISTERS - Command Line Mode")
    print("="*80)
    print(f"Address: {address} (0x{address:04X})")
    print(f"Count: {len(values)} register(s)")
    print(f"Values: {[f'{v} (0x{v:04X})' for v in values]}")
    print("="*80 + "\n")

    if len(values) == 1:
        success = await monitor.write_holding_register(address, values[0])
    else:
        success = await monitor.write_holding_registers(address, values)

    if success:
        print("✅ Write operation completed successfully!")
    else:
        print("❌ Write operation failed!")

    return success


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Modbus Monitor with Read/Write Support',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Read only (monitor mode):
    uv run python example_config.py

  Write single register:
    uv run python example_config.py --write --address 10 --values 1234

  Write multiple registers (decimal):
    uv run python example_config.py --write --address 10 --values 100,200,300

  Write multiple registers (hex):
    uv run python example_config.py --write --address 10 --values 0x64,0xC8,0x12C

  Interactive write mode:
    uv run python example_config.py --write-interactive

  Write then monitor:
    uv run python example_config.py --write --address 10 --values 1234 --monitor
        """
    )

    parser.add_argument('--write', action='store_true',
                       help='Enable write mode')
    parser.add_argument('--write-interactive', action='store_true',
                       help='Interactive write mode (prompts for address and values)')
    parser.add_argument('--address', type=int,
                       help='Register address to write to')
    parser.add_argument('--values', type=str,
                       help='Comma-separated values to write (supports hex with 0x prefix)')
    parser.add_argument('--monitor', action='store_true',
                       help='Start monitoring after write operation')
    parser.add_argument('--no-monitor', action='store_true',
                       help='Skip monitoring mode (default when using --write)')

    return parser.parse_args()


async def main():
    """Configure and run the Modbus monitor"""

    # Parse command-line arguments first
    args = parse_arguments()

    # Load configuration first (before logging setup to use log_level from config)
    cfg = load_config()

    # Setup logging with level from configuration
    logging.basicConfig(
        level=getattr(logging, cfg['log_level']),
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # ===== Original hardcoded configuration (COMMENTED OUT - Now using config files) =====
    # config = ModbusConfig(
    #     host='192.168.30.24',      # Change to your Modbus device IP
    #     port=502,                  # Standard Modbus TCP port
    #     device_id=1,               # Modbus device ID (slave ID)
    #     poll_interval=2.0,         # Poll every 2 seconds
    #     timeout=3.0,               # 3 second timeout
    #     retries=3                  # Retry 3 times on failure
    # )
    # START_ADDRESS = 1         # Starting address (0x0001 in the screenshot)
    # END_ADDRESS = 26          # Ending address (0x001A = 26 in decimal)

    # Configure Modbus connection from loaded configuration
    config = ModbusConfig(
        host=cfg['host'],
        port=cfg['port'],
        device_id=cfg['device_id'],
        poll_interval=cfg['poll_interval'],
        timeout=cfg['timeout'],
        retries=cfg['retries']
    )

    # Create monitor instance
    monitor = AsyncModbusMonitor(config)

    # ===== Configure Holding Registers to Monitor =====
    # Register range is now loaded from configuration file
    # Format: (start_address, count, register_type, name)

    # Get register range from configuration
    START_ADDRESS = cfg['start_address']
    END_ADDRESS = cfg['end_address']
    COUNT = END_ADDRESS - START_ADDRESS + 1

    # Add the holding register range
    monitor.add_register(
        address=START_ADDRESS,
        count=COUNT,
        register_type='holding',
        name=f'Holding_Registers_{START_ADDRESS}-{END_ADDRESS}'
    )

    # Optional: Add more register ranges if needed
    # monitor.add_register(100, 10, 'holding', 'Additional_Holding_Regs')

    # Input Registers (Read Only) - uncomment if needed
    # monitor.add_register(100, 8, 'input', 'Temperature_Sensors')

    # Coils (Digital Outputs) - uncomment if needed
    # monitor.add_register(0, 16, 'coils', 'Output_Controls')

    # Discrete Inputs (Digital Inputs) - uncomment if needed
    # monitor.add_register(100, 8, 'discrete_inputs', 'Alarm_Status')
    
    print("\n" + "="*80)
    print("📡 MODBUS MONITOR - Holding Registers (HEX to Decimal Converter)")
    print("="*80)
    print(f"Configuration    : {'✓ Loaded from config file' if Path('.env').exists() or Path('config.conf').exists() else '⚠ Using defaults'}")
    print(f"Target Device    : {config.host}:{config.port}")
    print(f"Device ID        : {config.device_id}")
    print(f"Poll Interval    : {config.poll_interval}s")
    print(f"Register Range   : {START_ADDRESS} to {END_ADDRESS} ({COUNT} registers)")
    print(f"Address Range    : 0x{START_ADDRESS:04X} to 0x{END_ADDRESS:04X}")
    print("="*80)

    try:
        # Connect to Modbus device
        if not await monitor.connect():
            logging.error("Failed to connect to Modbus device")
            return

        # ===== Handle write operations =====
        if args.write_interactive:
            # Interactive write mode
            await write_registers_interactive(monitor)
            # After interactive write, ask if user wants to monitor
            if not args.monitor:
                return
        elif args.write:
            # Command-line write mode
            if not args.address:
                logging.error("--address is required when using --write")
                return
            if not args.values:
                logging.error("--values is required when using --write")
                return

            # Parse values (support both hex and decimal)
            try:
                values_str = [v.strip() for v in args.values.split(',')]
                values = []
                for v_str in values_str:
                    if v_str.lower().startswith('0x'):
                        values.append(int(v_str, 16))
                    else:
                        values.append(int(v_str))

                # Validate values
                for v in values:
                    if v < 0 or v > 65535:
                        logging.error(f"Value {v} out of range (0-65535)")
                        return

                # Perform write
                await write_from_args(monitor, args.address, values)

                # Check if we should continue to monitor
                if args.no_monitor:
                    return
                # If --monitor is explicitly set or neither flag is set, continue to monitoring
                if not args.monitor and not args.no_monitor:
                    # Default behavior after write: exit
                    return

            except ValueError as e:
                logging.error(f"Invalid value format: {e}")
                return

        # ===== Start monitoring mode =====
        print("Press Ctrl+C to stop monitoring\n")
        await monitor.monitor_continuously(data_callback=data_processor)

    except KeyboardInterrupt:
        print("\n⏹️  Stopping monitor...")
        monitor.stop()

    except Exception as e:
        logging.error(f"Error: {e}")
        monitor.stop()


if __name__ == "__main__":
    asyncio.run(main())
