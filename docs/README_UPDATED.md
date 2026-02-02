# Async Modbus Monitor

一個基於 Python asyncio 的異步 Modbus 數據監控系統，提供 CLI 工具、FastAPI 後端服務和 Vue 3 前端界面，支持完整的 Modbus TCP 讀寫操作。

## 📋 專案概述

本專案是一個全端 (Full-stack) Modbus 監控解決方案，包含：
- **核心 Python 模組**: 異步 Modbus 客戶端庫
- **CLI 工具**: 命令列監控與讀寫工具
- **REST API 後端**: FastAPI 服務器，提供 HTTP 接口
- **Web 前端**: Vue 3 現代化用戶界面
- **數據存儲**: Redis 時序數據儲存
- **容器化部署**: Docker Compose 一鍵部署

## 📁 專案結構

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
