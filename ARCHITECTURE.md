# AEval Backend Architecture Documentation

## Table of Contents

1. [System Overview](#system-overview)
2. [Component Architecture](#component-architecture)
3. [Data Models](#data-models)
4. [Class Diagrams](#class-diagrams)
5. [State Machines](#state-machines)
6. [Deployment Architecture](#deployment-architecture)
7. [Security Architecture](#security-architecture)
8. [Evolution Roadmap](#evolution-roadmap)

---

## System Overview

### High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        FE[Frontend: AEvalTrae<br/>React + TypeScript]
    end

    subgraph "API Gateway Layer"
        API[FastAPI Server<br/>Port: 8000]
        CORS[CORS Middleware]
    end

    subgraph "Application Layer"
        Router[API Router]
        ChatSvc[ChatService<br/>Singleton]
        DataSvc[DataService<br/>With Caching]
        Agent[EvaluationAgent<br/>LLM Wrapper]
    end

    subgraph "Data Layer"
        JSON[JSON Files<br/>datasets.json<br/>metrics.json<br/>scenarios.json<br/>agents.json]
    end

    subgraph "External Services"
        ZAI[z.ai LLM API<br/>Model: glm-4.7]
    end

    FE -->|HTTPS/WSS| API
    API --> CORS
    CORS --> Router
    Router --> ChatSvc
    ChatSvc --> DataSvc
    ChatSvc --> Agent
    DataSvc --> JSON
    Agent --> ZAI

    style FE fill:#e3f2fd
    style API fill:#c8e6c9
    style ChatSvc fill:#fff9c4
    style Agent fill:#f3e5f5
    style ZAI fill:#ffccbc
    style JSON fill:#eceff1
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **API Framework** | FastAPI 0.104+ | High-performance async API |
| **Validation** | Pydantic v2 | Data validation and serialization |
| **LLM Client** | zhipuai 2.1.5+ | z.ai API integration |
| **Configuration** | pydantic-settings | Environment-based settings |
| **Testing** | pytest | Unit and integration tests |
| **Server** | uvicorn | ASGI server |

---

## Component Architecture

### Module Structure

```mermaid
graph LR
    subgraph "app/"
        main[main.py<br/>FastAPI App]
        config[config.py<br/>Settings]

        subgraph "models/"
            Dataset[dataset.py]
            Metric[metric.py]
            Scenario[scenario.py]
            Agent[agent.py]
            Rec[recommendation.py]
        end

        subgraph "services/"
            DataSvc[data_service.py<br/>Data Loader]
            ChatSvc[chat_service.py<br/>Orchestrator]
        end

        subgraph "agents/"
            EvalAgent[evaluation_agent.py<br/>Intent + Recommendation]
        end

        subgraph "api/"
            ChatAPI[chat.py<br/>Endpoints]
        end
    end

    main --> Router
    Router --> ChatAPI
    ChatAPI --> ChatSvc
    ChatSvc --> DataSvc
    ChatSvc --> EvalAgent
    EvalAgent --> Dataset
    EvalAgent --> Metric
    EvalAgent --> Scenario
    EvalAgent --> Agent
    ChatAPI --> Rec

    style main fill:#c8e6c9
    style config fill:#fff9c4
    style ChatSvc fill:#e1f5fe
    style EvalAgent fill:#f3e5f5
```

### Component Responsibilities

#### main.py
- **Responsibility**: Application bootstrap
- **Dependencies**: None (root module)
- **Functions**:
  - Initialize FastAPI app
  - Configure CORS
  - Register routers

#### config.py
- **Responsibility**: Configuration management
- **Dependencies**: pydantic-settings
- **Functions**:
  - Load from .env file
  - Type-safe settings access
  - Default value handling

#### models/
- **Responsibility**: Data contracts
- **Dependencies**: Pydantic
- **Functions**:
  - Request/response validation
  - JSON serialization/deserialization
  - Type hints and IDE support

#### services/
- **Responsibility**: Business logic
- **Dependencies**: Models, agents
- **Functions**:
  - Data loading with caching
  - Request orchestration
  - Singleton lifecycle management

#### agents/
- **Responsibility**: AI/LLM integration
- **Dependencies**: zhipuai, models
- **Functions**:
  - Prompt engineering
  - LLM API communication
  - Response parsing and validation

#### api/
- **Responsibility**: HTTP interface
- **Dependencies**: Services, models
- **Functions**:
  - Request validation
  - Error handling
  - Response formatting

---

## Data Models

### Entity Relationship Diagram

```mermaid
erDiagram
    DATASET ||--o{ RECOMMENDATION : "is selected for"
    METRIC ||--o{ RECOMMENDATION : "are selected for"
    SCENARIO ||--|| RECOMMENDATION : "defines"
    AGENT ||--|| RECOMMENDATION : "is evaluated"
    CHAT_REQUEST ||--|| CHAT_RESPONSE : "generates"
    CHAT_RESPONSE ||--o| RECOMMENDATION : "includes"

    DATASET {
        string id PK
        string name
        string description
        string[] tags
        string size
        int total_records
        string file_format
        float metadata_quality_score
        string application_context
        datetime created_at
    }

    METRIC {
        string id PK
        string name
        string category
        string description
        string cost "Low|Medium|High"
    }

    SCENARIO {
        string id PK
        string name
        string description
        string[] recommended_metrics
    }

    AGENT {
        string id PK
        string name
        string type
        string description
        string[] capabilities
    }

    RECOMMENDATION {
        DATASET dataset
        METRIC[] metrics
        AGENT agent
        SCENARIO scenario
        string reason
    }

    CHAT_REQUEST {
        string message "1-10000 chars"
    }

    CHAT_RESPONSE {
        string content
        RECOMMENDATION recommendation
        string[] quick_replies
    }
```

### Model Hierarchy

```mermaid
classDiagram
    class Pydantic~BaseModel~ {
        <<abstract>>
        +model_config: dict
    }

    class Dataset {
        +str: id
        +str: name
        +str: description
        +List[str]: tags
        +str: size
        +Optional[int]: total_records
        +str: file_format
        +float: metadata_quality_score
        +Optional[str]: application_context
        +Optional[datetime]: created_at
    }

    class Metric {
        +str: id
        +str: name
        +str: category
        +str: description
        +Literal: cost
    }

    class Scenario {
        +str: id
        +str: name
        +str: description
        +Optional[List[str]]: recommended_metrics
    }

    class AgentModel {
        +str: id
        +str: name
        +str: type
        +str: description
        +Optional[List[str]]: capabilities
    }

    class Recommendation {
        +Dataset: dataset
        +List[Metric]: metrics
        +AgentModel: agent
        +Scenario: scenario
        +str: reason
    }

    class ChatRequest {
        +str: message
        +validate_message() str
    }

    class ChatResponse {
        +str: content
        +Optional[Recommendation]: recommendation
        +List[str]: quick_replies
    }

    Pydantic <|-- Dataset
    Pydantic <|-- Metric
    Pydantic <|-- Scenario
    Pydantic <|-- AgentModel
    Pydantic <|-- Recommendation
    Pydantic <|-- ChatRequest
    Pydantic <|-- ChatResponse

    Recommendation --> Dataset
    Recommendation --> Metric
    Recommendation --> AgentModel
    Recommendation --> Scenario
    ChatResponse --> Recommendation
```

---

## Class Diagrams

### Service Layer Classes

```mermaid
classDiagram
    class DataService {
        -Path: data_dir
        -Optional[List[Dataset]]: _datasets
        -Optional[List[Metric]]: _metrics
        -Optional[List[Scenario]]: _scenarios
        -Optional[List[AgentModel]]: _agents
        +load_datasets() List[Dataset]
        +load_metrics() List[Metric]
        +load_scenarios() List[Scenario]
        +load_agents() List[AgentModel]
        -_load_json(file, model) List
    }

    class ChatService {
        -EvaluationAgent: agent
        -DataService: data_service
        -bool: _initialized
        +__init__()
        +ensure_initialized()
        +process_message(message) ChatResponse
    }

    class EvaluationAgent {
        -Optional[ZhipuAI]: client
        -str: SYSTEM_PROMPT
        +__init__()
        +initialize()
        +process_request(input, data) Tuple
        -_build_context(data) str
        -_build_recommendation(result, data) Recommendation
        -_generate_response(result, rec) str
    }

    class Settings {
        +str: zai_api_key
        +str: zai_model
        +str: api_host
        +int: api_port
        +float: agent_temperature
        +int: agent_max_tokens
        +str: data_dir
    }

    ChatService --> DataService
    ChatService --> EvaluationAgent
    EvaluationAgent --> Settings
```

### API Layer Classes

```mermaid
classDiagram
    class FastAPI {
        +FastAPI(title, version)
        +add_middleware()
        +include_router()
        +get(path)
    }

    class APIRouter {
        +APIRouter()
        +post(path, response_model)
    }

    class ChatEndpoint {
        +chat(request, service) ChatResponse
    }

    class CORSMiddleware {
        +allow_origins
        +allow_credentials
        +allow_methods
        +allow_headers
    }

    FastAPI --> CORSMiddleware
    FastAPI --> APIRouter
    APIRouter --> ChatEndpoint
```

---

## State Machines

### Chat Service Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Uninitialized: __init__
    Uninitialized --> Initializing: ensure_initialized()
    Initializing --> Initialized: agent.initialize()
    Initialized --> Processing: process_message()
    Processing --> DataLoading: Load data
    DataLoading --> AgentProcessing: Call agent
    AgentProcessing --> Responding: Build response
    Responding --> Initialized: Return response

    note right of Initializing
        Singleton pattern
        Only happens once
    end note

    note right of Processing
        Async operation
        Non-blocking
    end note
```

### Data Service Cache States

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> CacheMiss: First load request
    Created --> CacheHit: Subsequent requests
    CacheMiss --> FileReading: Read JSON
    FileReading --> Parsing: Parse JSON
    Parsing --> Cached: Store in memory
    Cached --> [*]: Return data
    CacheHit --> [*]: Return cached data

    note right of Cached
        _datasets, _metrics,
        _scenarios, _agents
        = None until loaded
    end note
```

### Request Processing States

```mermaid
stateDiagram-v2
    [*] --> Received: POST /api/chat

    Received --> Validating: Pydantic validation
    Validating --> Valid: Pass
    Validating --> ValidationError: Fail

    ValidationError --> [*]: 422 Response

    Valid --> Processing: ChatService
    Processing --> DataLoad: Load JSON files
    DataLoad --> DataError: File not found
    DataLoad --> LLMCall: Agent process

    DataError --> [*]: 500 Response

    LLMCall --> LLMError: API fail
    LLMCall --> ResponseParse: Got response

    LLMError --> [*]: 500 Response

    ResponseParse --> ParseError: Invalid JSON
    ResponseParse --> MissingFields: Validation fail
    ResponseParse --> Success: All valid

    ParseError --> [*]: 500 Response
    MissingFields --> [*]: 500 Response

    Success --> [*]: 200 ChatResponse
```

---

## Deployment Architecture

### Development Environment

```mermaid
graph TB
    subgraph "Developer Machine"
        subgraph "Frontend Terminal"
            FE[cd AEvalTrae<br/>npm run dev<br/>:5173]
        end

        subgraph "Backend Terminal"
            BE[cd aeval-backend/backend<br/>source venv/bin/activate<br/>uvicorn app.main:app<br/>:8000]
        end

        subgraph "File System"
            VEnv[venv/<br/>Python 3.10+]
            Env[.env<br/>ZAI_API_KEY]
            Data[data/<br/>*.json files]
        end

        Browser[Browser<br/>localhost:5173]
    end

    Browser --> FE
    FE --> BE
    BE --> VEnv
    BE --> Env
    BE --> Data

    style Browser fill:#e3f2fd
    style FE fill:#c8e6c9
    style BE fill:#fff9c4
```

### Production Deployment (Future)

```mermaid
graph TB
    subgraph "DMZ"
        LB[Load Balancer<br/>Nginx/ALB]
    end

    subgraph "Application Layer"
        App1[FastAPI Instance 1<br/>uvicorn]
        App2[FastAPI Instance 2<br/>uvicorn]
        AppN[FastAPI Instance N<br/>uvicorn]
    end

    subgraph "Data Layer"
        DB[(PostgreSQL<br/>or MongoDB)]
        Cache[Redis<br/>Session Cache]
    end

    subgraph "External Services"
        LLM[z.ai LLM API]
    end

    LB --> App1
    LB --> App2
    LB --> AppN

    App1 --> DB
    App2 --> DB
    AppN --> DB

    App1 --> Cache
    App2 --> Cache
    AppN --> Cache

    App1 --> LLM
    App2 --> LLM
    AppN --> LLM

    style LB fill:#ffccbc
    style DB fill:#c8e6c9
    style Cache fill:#fff9c4
    style LLM fill:#f3e5f5
```

### Docker Deployment (Future)

```mermaid
graph TB
    subgraph "Docker Network"
        subgraph "frontend-container"
            FE[Nginx<br/>React Build]
        end

        subgraph "backend-container"
            App[Uvicorn<br/>FastAPI]
        end

        subgraph "data-volume"
            JSON[JSON Files<br/>Mount]
        end
    end

    subgraph "Docker Compose"
        DC[docker-compose.yml]
    end

    FE --> App
    App --> JSON
    DC --> FE
    DC --> App

    style DC fill:#e3f2fd
    style FE fill:#c8e6c9
    style App fill:#fff9c4
```

---

## Security Architecture

### Current Security Model

```mermaid
graph TB
    subgraph "Security Layers"
        CORS[CORS Policy<br/>localhost:5173 only]
        Validation[Input Validation<br/>Pydantic Models]
        Error[Error Handling<br/>No sensitive data in errors]
        Env[Environment Variables<br/>.env file]
    end

    Request[Client Request] --> CORS
    CORS --> Validation
    Validation --> Error
    Error --> Env

    style CORS fill:#ffcdd2
    style Validation fill:#fff9c4
    style Error fill:#c8e6c9
    style Env fill:#b2dfdb
```

### Future Security Enhancements

```mermaid
graph TB
    subgraph "Enhanced Security Layers"
        Rate[Rate Limiting<br/>slowapi]
        Auth[Authentication<br/>JWT/OAuth2]
        RBAC[Role-Based Access<br/>Admin/User]
        Audit[Audit Logging<br/>All requests]
        Enc[Encryption<br/>TLS 1.3]
        Secrets[Secrets Management<br/>Vault/K8s Secrets]
    end

    Request[Client Request] --> Enc
    Enc --> Rate
    Rate --> Auth
    Auth --> RBAC
    RBAC --> Audit
    Audit --> Secrets

    style Rate fill:#ffcdd2
    style Auth fill:#fff9c4
    style RBAC fill:#c8e6c9
    style Audit fill:#b2dfdb
    style Enc fill:#ffccbc
```

---

## Evolution Roadmap

### Phase 1: Current (Prototype)

```mermaid
graph LR
    JSON[JSON Files] --> Service[Single Service]
    Service --> Agent[Single Agent]
    Agent --> LLM[LLM API]

    style JSON fill:#eceff1
    style Service fill:#c8e6c9
    style Agent fill:#fff9c4
    style LLM fill:#f3e5f5
```

### Phase 2: Database Migration

```mermaid
graph LR
    DB[(SQLite/PostgreSQL)] --> ORM[SQLAlchemy ORM]
    ORM --> Service[Service Layer]
    Service --> Agent[Agent Layer]
    Agent --> LLM[LLM API]

    style DB fill:#c8e6c9
    style ORM fill:#fff9c4
    style Service fill:#e1f5fe
    style Agent fill:#f3e5f5
    style LLM fill:#ffccbc
```

### Phase 3: Multi-Agent Architecture

```mermaid
graph TB
    subgraph "Agent Orchestrator"
        Orchestrator[Agent Orchestrator<br/>LangGraph/AutoGen]
    end

    subgraph "Specialized Agents"
        Intent[Intent Agent<br/>Classification]
        Data[Dataset Agent<br/>Recommendation]
        Metric[Metric Agent<br/>Selection]
        Scenario[Scenario Agent<br/>Configuration]
    end

    subgraph "Knowledge Base"
        DB[(Database)]
        Vector[Vector Store<br/>RAG]
    end

    Request[User Request] --> Orchestrator
    Orchestrator --> Intent
    Intent --> Data
    Data --> Metric
    Metric --> Scenario
    Intent --> DB
    Data --> DB
    Metric --> Vector
    Scenario --> DB

    style Orchestrator fill:#e1f5fe
    style Intent fill:#c8e6c9
    style Data fill:#fff9c4
    style Metric fill:#f3e5f5
    style Scenario fill:#ffccbc
    style DB fill:#eceff1
    style Vector fill:#b2dfdb
```

### Phase 4: Full Microservices

```mermaid
graph TB
    subgraph "API Gateway"
        Gateway[Kong/Traefik]
    end

    subgraph "Services"
        Chat[Chat Service]
        Data[Data Service]
        Agent[Agent Service]
        Eval[Evaluation Service]
    end

    subgraph "Message Queue"
        Queue[RabbitMQ/Kafka]
    end

    subgraph "Data Layer"
        DB[(PostgreSQL)]
        Cache[Redis]
        Vector[Vector DB]
    end

    Gateway --> Chat
    Gateway --> Data
    Gateway --> Agent
    Gateway --> Eval

    Chat --> Queue
    Data --> Queue
    Agent --> Queue
    Eval --> Queue

    Chat --> DB
    Data --> DB
    Agent --> Vector
    Eval --> Cache

    style Gateway fill:#e1f5fe
    style Chat fill:#c8e6c9
    style Data fill:#fff9c4
    style Agent fill:#f3e5f5
    style Eval fill:#ffccbc
    style Queue fill:#ffe0b2
```

---

## Design Patterns Used

### 1. Singleton Pattern
```mermaid
classDiagram
    class ChatService {
        -static ChatService _chat_service
        -__init__()
        +static get_chat_service() ChatService
    }

    note for ChatService
        Single instance shared across
        all requests for efficiency
    end note
```

### 2. Repository Pattern (Future)
```mermaid
classDiagram
    class Repository {
        <<interface>>
        +find_all()
        +find_by_id()
        +create()
        +update()
        +delete()
    }

    class DatasetRepository {
        +find_all()
        +find_by_id()
        +create()
        +update()
        +delete()
    }

    class MetricRepository {
        +find_all()
        +find_by_id()
        +create()
        +update()
        +delete()
    }

    Repository <|-- DatasetRepository
    Repository <|-- MetricRepository
```

### 3. Factory Pattern (Future)
```mermaid
classDiagram
    class AgentFactory {
        <<static>>
        +create_agent(type) Agent
    }

    class Agent {
        <<abstract>>
        +process()
    }

    class IntentAgent {
        +process()
    }

    class RecommendationAgent {
        +process()
    }

    AgentFactory --> Agent
    Agent <|-- IntentAgent
    Agent <|-- RecommendationAgent
```

---

## Performance Considerations

### Current Performance Characteristics

| Component | Operation | Avg Time | Bottleneck |
|-----------|-----------|----------|------------|
| DataService | load_datasets() | 5-10ms | File I/O |
| DataService | load_metrics() | 5-10ms | File I/O |
| EvaluationAgent | LLM API call | 15-25s | Network/LLM |
| ChatService | Total request | 15-25s | LLM API |

### Optimization Opportunities

```mermaid
graph TB
    subgraph "Current"
        C1[Sync File I/O] --> C2[No Caching]
        C2 --> C3[Single LLM Call]
    end

    subgraph "Optimizations"
        O1[Async File I/O<br/>aiofiles]
        O2[Redis Cache<br/>TTL: 1hr]
        O3[Streaming Response<br/>SSE/WebSocket]
        O4[Request Batching<br/>N>1 requests]
    end

    C1 -.->|Upgrade to| O1
    C2 -.->|Add| O2
    C3 -.->|Enable| O3
    C3 -.->|Implement| O4

    style O1 fill:#c8e6c9
    style O2 fill:#fff9c4
    style O3 fill:#e1f5fe
    style O4 fill:#f3e5f5
```

---

## Monitoring & Observability (Future)

### Metrics to Track

```mermaid
graph TB
    subgraph "Application Metrics"
        QPS[Queries Per Second]
        Latency[Request Latency<br/>p50, p95, p99]
        Error[Error Rate<br/>4xx, 5xx]
        Active[Active Requests]
    end

    subgraph "Business Metrics"
        Intent[Intent Accuracy]
        Rec[Recommendation Success]
        User[User Satisfaction]
    end

    subgraph "Infrastructure Metrics"
        CPU[CPU Usage]
        Mem[Memory Usage]
        Disk[Disk I/O]
        Net[Network I/O]
    end

    subgraph "LLM Metrics"
        Token[Token Usage]
        LLM_Latency[LLM Latency]
        Cost[API Cost]
    end

    style QPS fill:#c8e6c9
    style Latency fill:#fff9c4
    style Error fill:#ffcdd2
    style Token fill:#e1f5fe
```

---

## Appendix

### File Reference

| File | Lines of Code | Purpose |
|------|---------------|---------|
| `main.py` | 26 | FastAPI bootstrap |
| `config.py` | 30 | Configuration |
| `models/dataset.py` | 23 | Dataset model |
| `models/metric.py` | 15 | Metric model |
| `models/scenario.py` | 16 | Scenario model |
| `models/agent.py` | 17 | Agent model |
| `models/recommendation.py` | 39 | Request/Response models |
| `services/data_service.py` | 107 | Data loading |
| `services/chat_service.py` | 61 | Chat orchestration |
| `agents/evaluation_agent.py` | 232 | LLM agent |
| `api/chat.py` | 35 | Chat endpoint |

### Total Lines of Code

```
Language      Files    Lines    Code    Comments    Blanks
──────────────────────────────────────────────────────────
Python           11      601      450          50        101
JSON             4       200      200           0          0
──────────────────────────────────────────────────────────
Total            15      801      650          50        101
```

---

**Document Version**: 1.0.0
**Last Updated**: 2026-02-03
**Maintainer**: AEval Backend Team
