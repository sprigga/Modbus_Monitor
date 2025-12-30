#!/usr/bin/env python3
"""
Configuration Management Module
Uses pydantic-settings to manage application configuration from environment variables and config files
"""

from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List
from functools import lru_cache


class RedisConfig(BaseModel):
    """Redis connection configuration"""
    host: str = "localhost"
    port: int = 6379
    password: Optional[str] = None
    db: int = 0

    @validator('port')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v


class RegisterRangeConfig(BaseModel):
    """Configuration for register ranges to monitor"""
    start_address: int = 1
    count: int = 1
    register_type: str = "holding"
    name: Optional[str] = None

    @validator('register_type')
    def validate_register_type(cls, v):
        allowed_types = ['holding', 'input', 'coils', 'discrete_inputs']
        if v not in allowed_types:
            raise ValueError(f'Register type must be one of: {allowed_types}')
        return v

    @validator('count')
    def validate_count(cls, v):
        if v < 1 or v > 1000:  # Reasonable limit
            raise ValueError('Count must be between 1 and 1000')
        return v


class ModbusConfig(BaseModel):
    """
    Configuration for Modbus connection and monitoring
    """
    host: str
    port: int = 502
    device_id: int = 1
    poll_interval: float = 2.0
    timeout: float = 3.0
    retries: int = 3

    # Register configuration
    register_ranges: List[RegisterRangeConfig] = [
        RegisterRangeConfig(start_address=1, count=26, register_type="holding")
    ]

    @validator('port')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v

    @validator('device_id')
    def validate_device_id(cls, v):
        if not 1 <= v <= 247:  # Valid Modbus device ID range
            raise ValueError('Device ID must be between 1 and 247')
        return v

    @validator('poll_interval')
    def validate_poll_interval(cls, v):
        if v <= 0:
            raise ValueError('Poll interval must be greater than 0')
        return v

    @validator('timeout')
    def validate_timeout(cls, v):
        if v <= 0:
            raise ValueError('Timeout must be greater than 0')
        return v

    @validator('retries')
    def validate_retries(cls, v):
        if v < 0:
            raise ValueError('Retries cannot be negative')
        return v


class APIConfig(BaseModel):
    """API server configuration"""
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins: List[str] = ["*"]

    @validator('port')
    def validate_port(cls, v):
        if not 1 <= v <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        return v


class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class Settings(BaseSettings):
    """Main application settings configuration"""
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_prefix='',  # 移除前綴，因為 .env 中的變數已經有 MODBUS_ 前綴
        case_sensitive=False,
        extra='ignore'  # 忽略額外的環境變數
    )

    # Modbus configuration - 從環境變數讀取配置
    # 原有的程式碼: modbus: ModbusConfig = ModbusConfig()
    # 問題: ModbusConfig 需要 host 參數，直接實例化會導致 ValidationError
    # 解決方案: 使用 validator 從環境變數構建配置，使用 None 作為預設值
    modbus: Optional[ModbusConfig] = None

    # Redis configuration
    redis: Optional[RedisConfig] = None

    # API configuration
    api: Optional[APIConfig] = None

    # Logging configuration
    logging: Optional[LoggingConfig] = None

    # Configuration for register ranges (alternative to nested structure)
    # These can be used to override the nested register_ranges
    start_address: Optional[int] = Field(None, alias='START_ADDRESS')
    end_address: Optional[int] = Field(None, alias='END_ADDRESS')
    input_register_start: Optional[int] = Field(None, alias='INPUT_REGISTER_START')
    input_register_count: Optional[int] = Field(None, alias='INPUT_REGISTER_COUNT')
    coils_start: Optional[int] = Field(None, alias='COILS_START')
    coils_count: Optional[int] = Field(None, alias='COILS_COUNT')
    discrete_inputs_start: Optional[int] = Field(None, alias='DISCRETE_INPUTS_START')
    discrete_inputs_count: Optional[int] = Field(None, alias='DISCRETE_INPUTS_COUNT')

    @validator('modbus', pre=True, always=True)
    def parse_modbus_config(cls, v):
        """從環境變數解析 Modbus 配置"""
        import os
        from dotenv import load_dotenv

        # 確保載入 .env 文件
        load_dotenv()

        # 如果已經是 ModbusConfig 實例，直接返回
        # 但要檢查是否從環境變數創建，如果不是則重新創建
        if isinstance(v, ModbusConfig):
            return v

        # 從環境變數讀取配置
        host = os.getenv('MODBUS_HOST', '192.168.30.20')
        port = int(os.getenv('MODBUS_PORT', '502'))
        device_id = int(os.getenv('MODBUS_DEVICE_ID', '1'))
        poll_interval = float(os.getenv('MODBUS_POLL_INTERVAL', '2.0'))
        timeout = float(os.getenv('MODBUS_TIMEOUT', '3.0'))
        retries = int(os.getenv('MODBUS_RETRIES', '3'))

        return ModbusConfig(
            host=host,
            port=port,
            device_id=device_id,
            poll_interval=poll_interval,
            timeout=timeout,
            retries=retries
        )

    @validator('redis', pre=True, always=True)
    def parse_redis_config(cls, v):
        """從環境變數解析 Redis 配置"""
        import os
        from dotenv import load_dotenv

        load_dotenv()

        # 如果已經是 RedisConfig 實例，直接返回
        if isinstance(v, RedisConfig):
            return v

        # 從環境變數讀取配置
        host = os.getenv('REDIS_HOST', 'localhost')
        port = int(os.getenv('REDIS_PORT', '6379'))
        password = os.getenv('REDIS_PASSWORD')
        db = int(os.getenv('REDIS_DB', '0'))

        return RedisConfig(
            host=host,
            port=port,
            password=password,
            db=db
        )

    @validator('api', pre=True, always=True)
    def parse_api_config(cls, v):
        """從環境變數解析 API 配置"""
        import os
        from dotenv import load_dotenv

        load_dotenv()

        # 如果已經是 APIConfig 實例，直接返回
        if isinstance(v, APIConfig):
            return v

        # 從環境變數讀取配置
        host = os.getenv('API_HOST', '0.0.0.0')
        port = int(os.getenv('API_PORT', '8000'))
        debug = os.getenv('API_DEBUG', 'False').lower() == 'true'
        cors_origins_str = os.getenv('API_CORS_ORIGINS', '*')
        cors_origins = [origin.strip() for origin in cors_origins_str.split(',')]

        return APIConfig(
            host=host,
            port=port,
            debug=debug,
            cors_origins=cors_origins
        )

    @validator('logging', pre=True, always=True)
    def parse_logging_config(cls, v):
        """從環境變數解析日誌配置"""
        import os
        from dotenv import load_dotenv

        load_dotenv()

        # 如果已經是 LoggingConfig 實例，直接返回
        if isinstance(v, LoggingConfig):
            return v

        # 從環境變數讀取配置
        level = os.getenv('LOG_LEVEL', 'INFO')
        format_str = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        return LoggingConfig(
            level=level,
            format=format_str
        )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    # 確保載入 .env 文件
    from dotenv import load_dotenv
    load_dotenv()
    return Settings()


# Alternative simple configuration class for backward compatibility
class SimpleModbusConfig:
    """
    Simple configuration class for backward compatibility
    This maintains the original dataclass structure but with configurable defaults
    """

    def __init__(
        self,
        host: str = "192.168.30.24",
        port: int = 502,
        device_id: int = 1,
        poll_interval: float = 2.0,
        timeout: float = 3.0,
        retries: int = 3
    ):
        self.host = host
        self.port = port
        self.device_id = device_id
        self.poll_interval = poll_interval
        self.timeout = timeout
        self.retries = retries