# Architecture Overview

This page provides a comprehensive overview of the Pet Paradise Shop system architecture.

## System Architecture

The system follows a layered architecture with clear separation of concerns:

```mermaid
graph TB
    subgraph "User Layer"
        U[User/Customer]
    end
    
    subgraph "Presentation Layer"
        CL[Chainlit Chat Interface<br/>Port: 8001]
    end
    
    subgraph "AI Orchestration Layer"
        AZ[Azure OpenAI GPT-4<br/>Structured Outputs]
        TC[Tool Calling Engine<br/>Pydantic Validation]
    end
    
    subgraph "Application Layer"
        API[FastAPI REST API<br/>Port: 8000]
        T1[browse_pets Tool]
        T2[place_order Tool]
        T3[check_order_status Tool]
    end
    
    subgraph "Data Layer"
        DB[(MongoDB<br/>Port: 27017)]
        PETS[Pets Collection]
        ORDERS[Orders Collection]
    end
    
    subgraph "Observability Layer"
        OTEL[OpenTelemetry<br/>Collector]
        PROM[Prometheus<br/>Metrics]
        JAEGER[Jaeger<br/>Tracing]
    end
    
    U -->|Chat Messages| CL
    CL -->|API Calls| AZ
    AZ -->|Tool Decisions| TC
    TC -->|HTTP Requests| T1
    TC -->|HTTP Requests| T2
    TC -->|HTTP Requests| T3
    T1 -->|REST Calls| API
    T2 -->|REST Calls| API
    T3 -->|REST Calls| API
    API -->|Queries| DB
    DB -->|Data| PETS
    DB -->|Data| ORDERS
    
    API -.->|Traces| OTEL
    API -.->|Metrics| PROM
    OTEL -.->|Spans| JAEGER
    CL -.->|Traces| OTEL
    
    style U fill:#e3f2fd
    style CL fill:#c5e1a5
    style AZ fill:#ffccbc
    style API fill:#b2dfdb
    style DB fill:#f8bbd0
    style OTEL fill:#d1c4e9
    style PROM fill:#ffe0b2
    style JAEGER fill:#f48fb1
```

## Component Interaction Flow

```mermaid
sequenceDiagram
    participant User
    participant Chainlit
    participant Azure OpenAI
    participant Tools
    participant FastAPI
    participant MongoDB
    participant OpenTelemetry
    participant Jaeger
    
    User->>Chainlit: "Show me dogs under $1000"
    Chainlit->>OpenTelemetry: Start trace span
    Chainlit->>Azure OpenAI: Send message + tool definitions
    
    Azure OpenAI->>Azure OpenAI: Analyze request
    Azure OpenAI->>Tools: Call browse_pets(pet_type="dog", max_price=1000)
    
    Tools->>OpenTelemetry: Create tool span
    Tools->>FastAPI: GET /pets?pet_type=dog&max_price=1000
    
    FastAPI->>OpenTelemetry: Create API span
    FastAPI->>MongoDB: Query pets collection
    MongoDB-->>FastAPI: Return matching pets
    
    FastAPI-->>Tools: JSON response with pets
    FastAPI->>OpenTelemetry: Record metrics
    Tools-->>Azure OpenAI: Tool result
    
    Azure OpenAI->>Azure OpenAI: Generate response
    Azure OpenAI-->>Chainlit: Natural language response
    Chainlit-->>User: "I found 1 dog under $1000..."
    
    Chainlit->>OpenTelemetry: End trace span
    OpenTelemetry->>Jaeger: Export trace
```

## Data Flow Architecture

```mermaid
flowchart LR
    subgraph Input
        UI[User Input]
    end
    
    subgraph Validation["Multi-Layer Validation"]
        V1[Tool Input<br/>Validation]
        V2[API Request<br/>Validation]
        V3[Database<br/>Validation]
    end
    
    subgraph Processing
        P1[AI Processing]
        P2[Tool Execution]
        P3[Business Logic]
    end
    
    subgraph Storage
        S1[(MongoDB)]
    end
    
    subgraph Output
        O1[Structured<br/>Response]
        O2[UI Display]
    end
    
    UI --> V1
    V1 --> P1
    P1 --> P2
    P2 --> V2
    V2 --> P3
    P3 --> V3
    V3 --> S1
    S1 --> O1
    O1 --> O2
    O2 --> UI
    
    style V1 fill:#ffeb3b
    style V2 fill:#ffeb3b
    style V3 fill:#ffeb3b
    style O1 fill:#4caf50
```

## Technology Stack

```mermaid
mindmap
  root((Pet Paradise<br/>Shop))
    Frontend
      Chainlit
      Markdown UI
      Rich Formatting
    AI Layer
      Azure OpenAI
      GPT-4
      Structured Outputs
      Function Calling
    Backend
      FastAPI
      Async Operations
      REST API
      Pydantic
    Database
      MongoDB
      Motor Driver
      Document Store
    Observability
      OpenTelemetry
        Tracing
        Metrics
        Context Propagation
      Prometheus
        Metrics Collection
        Time Series DB
      Jaeger
        Distributed Tracing
        Span Analysis
    Validation
      Pydantic Models
      Type Safety
      Enums
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Docker Network"
        subgraph "Chat Service"
            CHAT[Chainlit Container<br/>Port: 8001]
        end
        
        subgraph "API Service"
            APIAPP[FastAPI Container<br/>Port: 8000]
        end
        
        subgraph "Database Service"
            MONGO[MongoDB Container<br/>Port: 27017]
        end
        
        subgraph "Observability Stack"
            OTELCOL[OpenTelemetry Collector<br/>Port: 4317, 4318]
            PROMDB[Prometheus<br/>Port: 9090]
            JAEGERUI[Jaeger UI<br/>Port: 16686]
        end
    end
    
    subgraph "External Services"
        AZURE[Azure OpenAI<br/>API]
    end
    
    CHAT -->|HTTP| APIAPP
    CHAT -->|API Calls| AZURE
    APIAPP -->|MongoDB Protocol| MONGO
    CHAT -.->|OTLP| OTELCOL
    APIAPP -.->|OTLP| OTELCOL
    APIAPP -.->|/metrics| PROMDB
    OTELCOL -.->|Spans| JAEGERUI
    PROMDB -.->|Scrape| APIAPP
    
    style AZURE fill:#0078d4
    style OTELCOL fill:#d1c4e9
    style PROMDB fill:#e37933
    style JAEGERUI fill:#66d9ef
```

## Security Architecture

```mermaid
flowchart TD
    A[External Request] --> B{Authentication}
    B -->|Valid| C[Rate Limiting]
    B -->|Invalid| Z[Reject]
    C --> D{Authorization}
    D -->|Authorized| E[Input Validation]
    D -->|Unauthorized| Z
    E -->|Valid| F[Business Logic]
    E -->|Invalid| Z
    F --> G[Data Access]
    G --> H{Data Validation}
    H -->|Valid| I[Response]
    H -->|Invalid| J[Error Handler]
    I --> K[Output Sanitization]
    J --> K
    K --> L[Encrypted Response]
    
    style B fill:#ff9800
    style D fill:#ff9800
    style E fill:#4caf50
    style H fill:#4caf50
    style K fill:#4caf50
    style Z fill:#f44336
```

## Key Architectural Principles

### 1. Separation of Concerns

Each layer has a specific responsibility:

- **UI Layer**: User interaction and display
- **AI Layer**: Natural language processing and tool orchestration
- **Application Layer**: Business logic and data manipulation
- **Data Layer**: Persistence and retrieval

### 2. Type Safety

Pydantic models ensure type correctness throughout:

```python
class Pet(BaseModel):
    id: str
    name: str
    type: PetType  # Enum for type safety
    price: float = Field(gt=0)  # Validation constraint
```

### 3. Async All the Way

Non-blocking I/O for scalability:

```python
async def browse_pets_tool(pet_type: Optional[str] = None):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE_URL}/pets")
```

### 4. Multi-Layer Validation

Validation at every boundary:

1. **Tool Input**: Pydantic validates before tool execution
2. **API Request**: FastAPI validates HTTP requests
3. **Database**: Models validate before persistence

### 5. Observability First

Built-in tracing and metrics:

- OpenTelemetry for distributed tracing
- Prometheus for metrics collection
- Jaeger for trace visualization
- Structured logging throughout

## Scalability Considerations

```mermaid
graph LR
    subgraph "Horizontal Scaling"
        LB[Load Balancer]
        API1[API Instance 1]
        API2[API Instance 2]
        API3[API Instance 3]
    end
    
    subgraph "Data Layer"
        MONGO1[(MongoDB<br/>Primary)]
        MONGO2[(MongoDB<br/>Secondary)]
        MONGO3[(MongoDB<br/>Secondary)]
    end
    
    subgraph "Cache Layer"
        REDIS[(Redis Cache)]
    end
    
    LB --> API1
    LB --> API2
    LB --> API3
    
    API1 --> REDIS
    API2 --> REDIS
    API3 --> REDIS
    
    API1 --> MONGO1
    API2 --> MONGO1
    API3 --> MONGO1
    
    MONGO1 -.Replication.-> MONGO2
    MONGO1 -.Replication.-> MONGO3
```

## Next Steps

- Explore [Component Details](components.md)
- Understand [Data Flow](data-flow.md)
- Learn about [Observability](../observability/overview.md)
