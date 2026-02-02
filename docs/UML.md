# Modbus Monitor UML Diagrams

## Component Diagram

```plantuml
@startuml ModbusMonitorComponentDiagram
!theme plain
skinparam packageStyle rectangle
skinparam componentStyle uml2

title Modbus Monitor System - Component Diagram

package "Frontend" as Frontend {
    component [Vue.js App] as VueApp
    component [HTML/CSS] as UI
    note right of VueApp
        Frontend Application
        - Vue 3 SPA
        - Real-time UI
        - User Interface
    end note
}

package "Backend API" as Backend {
    component [FastAPI] as FastAPI
    component [Modbus Service] as ModbusService
    component [Redis Client] as RedisClient

    note right of FastAPI
        FastAPI Application
        - REST API Server
        - Request Handling
        - CORS Support
    end note

    note right of ModbusService
        Modbus Service Layer
        - Modbus TCP Communication
        - Register Operations
        - Monitoring Logic
    end note

    note right of RedisClient
        Redis Data Store
        - Data Caching
        - Historical Data
        - Latest Data Storage
    end note
}

package "External Systems" as External {
    component [Modbus Device] as ModbusDevice
    component [User Browser] as Browser

    note right of ModbusDevice
        Physical Modbus Device
        - TCP/IP Connection
        - Holding Registers
        - Input Registers
        - Coils
        - Discrete Inputs
    end note
}

' Component relationships
Frontend --> Backend : HTTP/HTTPS API Calls
VueApp --> UI : User Interface Rendering
UI --> VueApp : Event Handling

Backend --> Backend : Internal Communication
FastAPI --> ModbusService : Modbus Operations
FastAPI --> RedisClient : Data Storage
ModbusService --> RedisClient : Data Persistence

Backend --> External : Modbus TCP/IP Connection
FastAPI --> ModbusDevice : Modbus Commands
ModbusService --> ModbusDevice : Read/Write Operations
ModbusService --> ModbusDevice : Connection Management

Browser --> Frontend : User Interaction

' Data flows
note top of FastAPI
    REST API Endpoints:
    - GET /api/config
    - POST /api/config
    - POST /api/connect
    - POST /api/disconnect
    - GET /api/status
    - POST /api/read
    - POST /api/write
    - POST /api/write_multiple
    - POST /api/start_monitoring
    - POST /api/stop_monitoring
    - GET /api/data/latest
    - GET /api/data/history
end note

note top of RedisClient
    Redis Data Structure:
    - modbus:latest (JSON)
    - modbus:history (Sorted Set)
end note

@enduml
```

### Component Description

#### Frontend Components
1. **Vue.js App** - Main single-page application built with Vue 3
   - Real-time data binding
   - User state management
   - API communication handling

2. **HTML/CSS** - User interface layer
   - Modern glass-morphism design
   - Responsive layout
   - Interactive components

#### Backend Components
1. **FastAPI** - REST API server
   - HTTP request handling
   - CORS middleware
   - API endpoint management
   - Data validation with Pydantic

2. **Modbus Service** - Modbus protocol layer
   - TCP client connection
   - Register read/write operations
   - Continuous monitoring
   - Error handling and retries

3. **Redis Client** - Data storage layer
   - Latest data caching
   - Historical data persistence
   - Fast data retrieval

#### External Systems
1. **Modbus Device** - Physical or simulated Modbus device
   - Supports Modbus TCP protocol
   - Multiple register types
   - Real-time data updates

2. **User Browser** - Client interface
   - Web application container
   - User interaction point

### Key Interfaces
- **API Interface**: RESTful JSON API between frontend and backend
- **Modbus Interface**: TCP-based protocol for device communication
- **Data Interface**: Redis pub/sub for data caching and retrieval
- **UI Interface**: User interaction through web browser

### Data Flow
1. User configures connection parameters via UI
2. Frontend sends API requests to backend
3. Backend establishes Modbus TCP connection
4. Modbus Service reads/writes register data
5. Data is stored in Redis for persistence
6. Frontend displays real-time data updates

@enduml