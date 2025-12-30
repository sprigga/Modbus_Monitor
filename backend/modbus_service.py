#!/usr/bin/env python3
"""
Modbus Service Module
Integrates async_modbus_monitor.py functionality with Redis storage
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import redis.asyncio as redis

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

# Import the new configuration system
from .config import SimpleModbusConfig, Settings, get_settings


# Keep the original dataclass for backward compatibility but with configurable defaults
@dataclass
class ModbusConfig:
    """
    Configuration for Modbus connection and monitoring
    DEPRECATED: Use SimpleModbusConfig or Settings.modbus instead
    """
    host: str = "192.168.30.24"
    port: int = 502
    device_id: int = 1
    poll_interval: float = 1.0
    timeout: float = 3.0
    retries: int = 3


@dataclass
class RegisterConfig:
    """Configuration for register monitoring"""
    address: int
    count: int = 1
    register_type: str = 'holding'  # holding, input, coils, discrete_inputs
    name: str = None


class ModbusService:
    """Enhanced Modbus service with Redis integration"""
    
    def __init__(self, config: ModbusConfig, redis_client: redis.Redis):
        self.config = config
        self.redis_client = redis_client
        self.client: Optional[AsyncModbusTcpClient] = None
        self.running = False
        self.logger = logging.getLogger(__name__)
        self.registers_to_monitor: List[RegisterConfig] = []
        
    def add_register(self, address: int, count: int = 1, 
                    register_type: str = 'holding', name: str = None):
        """Add a register to monitor"""
        reg_config = RegisterConfig(
            address=address, 
            count=count, 
            register_type=register_type,
            name=name or f"{register_type}_{address}"
        )
        self.registers_to_monitor.append(reg_config)
        
    async def connect(self) -> bool:
        """Connect to Modbus device"""
        try:
            self.client = AsyncModbusTcpClient(
                host=self.config.host,
                port=self.config.port,
                timeout=self.config.timeout,
                retries=self.config.retries
            )
            
            await self.client.connect()
            
            if self.client.connected:
                self.logger.info(f"Connected to Modbus device at {self.config.host}:{self.config.port}")
                return True
            else:
                self.logger.error("Failed to connect to Modbus device")
                return False
                
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from Modbus device"""
        if self.client:
            self.client.close()
            self.logger.info("Disconnected from Modbus device")
    
    def is_connected(self) -> bool:
        """Check if connected to Modbus device"""
        return self.client is not None and self.client.connected
    
    async def read_registers(self, address: int, count: int = 1, 
                           register_type: str = 'holding') -> Optional[Dict[str, Any]]:
        """Read registers and return formatted data"""
        if not self.client or not self.client.connected:
            return None
            
        try:
            if register_type == 'holding':
                result = await self.client.read_holding_registers(
                    address, count=count, device_id=self.config.device_id
                )
                values = result.registers if not result.isError() else None
                
            elif register_type == 'input':
                result = await self.client.read_input_registers(
                    address, count=count, device_id=self.config.device_id
                )
                values = result.registers if not result.isError() else None
                
            elif register_type == 'coils':
                result = await self.client.read_coils(
                    address, count=count, device_id=self.config.device_id
                )
                values = result.bits if not result.isError() else None
                
            elif register_type == 'discrete_inputs':
                result = await self.client.read_discrete_inputs(
                    address, count=count, device_id=self.config.device_id
                )
                values = result.bits if not result.isError() else None
                
            else:
                self.logger.error(f"Unknown register type: {register_type}")
                return None
            
            if values is not None:
                return {
                    'address': address,
                    'type': register_type,
                    'count': count,
                    'values': values[:count] if isinstance(values, list) else [values],
                    'timestamp': datetime.now().isoformat()
                }
            else:
                self.logger.error(f"Error reading registers at address {address}: {result}")
                return None
                
        except ModbusException as exc:
            self.logger.error(f"Modbus exception reading address {address}: {exc}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error reading address {address}: {e}")
            return None

    async def write_single_register(self, address: int, value: int) -> bool:
        """Write a single holding register"""
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
                self.logger.info(f"Successfully wrote value {value} to address {address}")
                return True
            else:
                self.logger.error(f"Error writing to address {address}: {result}")
                return False

        except ModbusException as exc:
            self.logger.error(f"Modbus exception writing to address {address}: {exc}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error writing to address {address}: {e}")
            return False

    async def write_multiple_registers(self, address: int, values: List[int]) -> bool:
        """Write multiple holding registers"""
        if not self.client or not self.client.connected:
            self.logger.error("Not connected to Modbus device")
            return False

        try:
            result = await self.client.write_registers(
                address=address,
                values=values,
                device_id=self.config.device_id
            )

            if not result.isError():
                self.logger.info(f"Successfully wrote {len(values)} registers starting at address {address}")
                return True
            else:
                self.logger.error(f"Error writing to address {address}: {result}")
                return False

        except ModbusException as exc:
            self.logger.error(f"Modbus exception writing to address {address}: {exc}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error writing to address {address}: {e}")
            return False

    async def store_data_to_redis(self, data: List[Dict[str, Any]]):
        """Store data to Redis"""
        try:
            # Store latest data
            latest_data = {
                'data': data,
                'timestamp': datetime.now().isoformat()
            }
            await self.redis_client.set("modbus:latest", json.dumps(latest_data))
            
            # Store to history (sorted set with timestamp as score)
            timestamp = datetime.now().timestamp()
            await self.redis_client.zadd(
                "modbus:history", 
                {json.dumps(latest_data): timestamp}
            )
            
            # Keep only last 1000 entries in history
            await self.redis_client.zremrangebyrank("modbus:history", 0, -1001)
            
        except Exception as e:
            self.logger.error(f"Error storing data to Redis: {e}")

    async def read_all_registers(self) -> List[Dict[str, Any]]:
        """Read all configured registers"""
        tasks = []
        for reg in self.registers_to_monitor:
            task = self.read_registers(reg.address, reg.count, reg.register_type)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)

        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, dict):
                # Add register name
                result['name'] = self.registers_to_monitor[i].name
                valid_results.append(result)
            elif isinstance(result, Exception):
                self.logger.error(f"Task failed with exception: {result}")

        return valid_results

    async def start_monitoring(self):
        """Start continuous monitoring and store data to Redis"""
        self.running = True
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        self.logger.info(f"Starting continuous monitoring (interval: {self.config.poll_interval}s)")
        
        while self.running:
            try:
                if not self.client or not self.client.connected:
                    self.logger.warning("Connection lost, attempting to reconnect...")
                    if not await self.connect():
                        consecutive_errors += 1
                        if consecutive_errors >= max_consecutive_errors:
                            self.logger.error("Max consecutive connection errors reached, stopping monitor")
                            break
                        await asyncio.sleep(self.config.poll_interval)
                        continue
                
                data = await self.read_all_registers()
                
                if data:
                    consecutive_errors = 0
                    # Store data to Redis
                    await self.store_data_to_redis(data)
                    self.logger.debug(f"Stored {len(data)} register readings to Redis")
                else:
                    consecutive_errors += 1
                    self.logger.warning(f"No data received (consecutive errors: {consecutive_errors})")
                
                if consecutive_errors >= max_consecutive_errors:
                    self.logger.error("Max consecutive read errors reached, stopping monitor")
                    break
                    
                await asyncio.sleep(self.config.poll_interval)
                
            except asyncio.CancelledError:
                self.logger.info("Monitor task cancelled")
                break
            except Exception as e:
                consecutive_errors += 1
                self.logger.error(f"Unexpected error in monitor loop: {e}")
                if consecutive_errors >= max_consecutive_errors:
                    self.logger.error("Max consecutive errors reached, stopping monitor")
                    break
                await asyncio.sleep(self.config.poll_interval)
        
        self.running = False

    def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False