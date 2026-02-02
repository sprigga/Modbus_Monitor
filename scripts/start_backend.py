#!/usr/bin/env python3
"""
Backend startup script for Modbus Monitor
"""

import uvicorn
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    print(f"Starting Modbus Monitor Backend on {host}:{port}")
    print("Make sure Redis is running on localhost:6379")
    
    # Start the server
    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )