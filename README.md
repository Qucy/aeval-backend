# AEval Backend

AI-Assisted Evaluation Configuration Backend - A Python FastAPI backend that provides AI-powered intent extraction and evaluation configuration recommendations.

## Features

- **AI-Powered Chat**: Uses z.ai API (OpenAI-compatible) for intelligent conversation
- **Intent Extraction**: Automatically classifies user evaluation goals
- **Smart Recommendations**: Suggests appropriate datasets, metrics, scenarios, and agents
- **RESTful API**: Clean FastAPI endpoints with automatic OpenAPI documentation
- **Async Support**: Built on async/await for high performance

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Configuration (env vars, settings)
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   ├── dataset.py
│   │   ├── metric.py
│   │   ├── scenario.py
│   │   ├── agent.py
│   │   └── recommendation.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── data_service.py  # Data loading service
│   │   └── chat_service.py # Chat orchestration service
│   ├── agents/              # AI agents
│   │   ├── __init__.py
│   │   └── evaluation_agent.py
│   └── api/                 # API endpoints
│       ├── __init__.py
│       └── chat.py          # Chat endpoint
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── fixtures.py
│   ├── test_agents.py
│   └── test_api.py
├── data/                    # Initial data
│   ├── datasets.json
│   ├── metrics.json
│   ├── scenarios.json
│   └── agents.json
├── requirements.txt
├── pyproject.toml
└── .env.example
```

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip or poetry
- z.ai API key

### Installation

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   ```

2. **Activate virtual environment**
   ```bash
   # On Linux/Mac
   source venv/bin/activate

   # On Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your z.ai API credentials:
   ```env
   ZAI_API_KEY=your_actual_api_key_here
   ZAI_BASE_URL=https://api.z.ai/v1
   ZAI_MODEL=gpt-4o-mini
   ```

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

   Interactive API docs: `http://localhost:8000/docs`

## Request Flow Architecture

### Complete Chat Request Sequence

```mermaid
sequenceDiagram
    autonumber
    participant Frontend as AEvalTrae Frontend
    participant FastAPI as FastAPI Server
    participant ChatAPI as Chat API Router
    participant ChatService as ChatService
    participant DataService as DataService
    participant Agent as EvaluationAgent
    participant LLM as z.ai LLM API
    participant FileSystem as JSON Files

    Frontend->>FastAPI: POST /api/chat {"message": "Test my RAG agent"}
    FastAPI->>ChatAPI: Router forwards request
    ChatAPI->>ChatAPI: Validate ChatRequest (Pydantic)
    ChatAPI->>ChatService: process_message(message)
    ChatService->>ChatService: ensure_initialized()

    par Load Evaluation Data
        ChatService->>DataService: load_datasets()
        DataService->>FileSystem: Read datasets.json
        FileSystem-->>DataService: JSON Data
        DataService->>DataService: Parse & Cache (List[Dataset])
        DataService-->>ChatService: List[Dataset]

        ChatService->>DataService: load_metrics()
        DataService->>FileSystem: Read metrics.json
        FileSystem-->>DataService: JSON Data
        DataService->>DataService: Parse & Cache (List[Metric])
        DataService-->>ChatService: List[Metric]

        ChatService->>DataService: load_scenarios()
        DataService->>FileSystem: Read scenarios.json
        FileSystem-->>DataService: JSON Data
        DataService->>DataService: Parse & Cache (List[Scenario])
        DataService-->>ChatService: List[Scenario]

        ChatService->>DataService: load_agents()
        DataService->>FileSystem: Read agents.json
        FileSystem-->>DataService: JSON Data
        DataService->>DataService: Parse & Cache (List[Agent])
        DataService-->>ChatService: List[Agent]
    and Initialize Agent
        ChatService->>Agent: initialize()
        Agent->>Agent: Create ZhipuAI client
    end

    ChatService->>Agent: process_request(message, data)

    Agent->>Agent: _build_context(data)
    Note over Agent: Format datasets, metrics,<br/>scenarios, agents as context

    Agent->>Agent: Build messages (system + user)

    Agent->>LLM: chat.completions.create()
    Note over Agent,LLM: Temperature: 0.7<br/>Max Tokens: 2000<br/>Model: glm-4.7

    LLM-->>Agent: Response (JSON with recommendations)
    Agent->>Agent: Strip markdown code blocks
    Agent->>Agent: Parse JSON response
    Agent->>Agent: Validate required fields
    Agent->>Agent: _build_recommendation(result, data)
    Agent->>Agent: _generate_response(result)
    Agent-->>ChatService: (content, recommendation)

    ChatService->>ChatService: Build ChatResponse
    ChatService->>ChatService: Add quick_replies
    ChatService-->>ChatAPI: ChatResponse

    ChatAPI-->>FastAPI: ChatResponse
    FastAPI-->>Frontend: JSON Response
```

### Data Loading & Caching Flow

```mermaid
sequenceDiagram
    autonumber
    participant Service as ChatService
    participant DataSvc as DataService
    participant Cache as Internal Cache
    participant Files as JSON Files

    Service->>DataSvc: load_datasets()

    alt Cache Miss (First Call)
        DataSvc->>Cache: Check _datasets
        Cache-->>DataSvc: None
        DataSvc->>Files: Open datasets.json
        Files-->>DataSvc: File Handle
        DataSvc->>DataSvc: json.load()
        DataSvc->>DataSvc: [Dataset(**d) for d in data]
        DataSvc->>Cache: Store parsed datasets
        Cache-->>DataSvc: Stored
        DataSvc-->>Service: List[Dataset]
    else Cache Hit (Subsequent Calls)
        DataSvc->>Cache: Check _datasets
        Cache-->>DataSvc: Cached List[Dataset]
        DataSvc-->>Service: List[Dataset] (from cache)
    end

    Note over DataSvc: Same pattern for:<br/>- load_metrics()<br/>- load_scenarios()<br/>- load_agents()
```

### LLM Interaction Detail

```mermaid
sequenceDiagram
    autonumber
    participant Agent as EvaluationAgent
    participant AsyncIO as asyncio.to_thread
    participant Client as ZhipuAI Client
    participant API as z.ai API

    Agent->>Agent: Build system prompt + context
    Note over Agent: SYSTEM_PROMPT:<br/>- Intent categories<br/>- JSON format required
    Note over Agent: CONTEXT:<br/>- All datasets<br/>- All metrics<br/>- All scenarios<br/>- All agents

    Agent->>Agent: Build messages array
    Note over Agent: [<br/>  {role: "system", content: "..."},<br/>  {role: "user", content: user_input}<br/>]

    Agent->>AsyncIO: to_thread(client.chat.completions.create)
    Note over Agent,AsyncIO: Non-blocking wrapper<br/>for sync SDK call

    AsyncIO->>Client: chat.completions.create()
    Client->>API: POST /chat/completions
    API-->>Client: Response

    Client-->>AsyncIO: CompletionResponse
    AsyncIO-->>Agent: CompletionResponse

    Agent->>Agent: Extract response.choices[0].message.content

    alt Response wrapped in markdown
        Agent->>Agent: Strip ```json ... ``` blocks
        Agent->>Agent: Parse JSON
    else Response is plain JSON
        Agent->>Agent: Parse JSON directly
    end

    Agent->>Agent: Validate required fields
    Note over Agent: Check: intent, dataset_id,<br/>metric_ids, scenario_id, agent_id

    alt Missing required fields
        Agent->>Agent: Raise ValueError
    else All fields present
        Agent->>Agent: Build Recommendation object
        Agent->>Agent: Generate friendly response
        Agent-->>Return: (content, recommendation)
    end
```

### Error Handling Flow

```mermaid
sequenceDiagram
    autonumber
    participant Frontend as Frontend
    participant API as Chat API
    participant Service as ChatService
    participant DataSvc as DataService
    participant Agent as EvaluationAgent

    Frontend->>API: POST /api/chat

    alt Input Validation Error
        API->>API: Pydantic validation fails
        API-->>Frontend: 422 Validation Error
        Note over API: Message empty,<br/>too long, or invalid
    else Data File Error
        API->>Service: process_message()
        Service->>DataSvc: load_datasets()
        DataSvc->>DataSvc: FileNotFoundError / ValueError
        DataSvc-->>Service: Exception
        Service-->>API: Exception
        API-->>Frontend: 500 Data file error
    else LLM API Error
        API->>Service: process_message()
        Service->>Agent: process_request()
        Agent->>Agent: LLM API call fails
        Agent-->>Service: ValueError
        Service-->>API: Exception
        API-->>Frontend: 500 Internal server error
    else Invalid LLM Response
        API->>Service: process_message()
        Service->>Agent: process_request()
        Agent->>Agent: JSON decode fails
        Agent->>Agent: Missing fields
        Agent-->>Service: ValueError
        Service-->>API: Exception
        API-->>Frontend: 500 Internal server error
    else Success
        API-->>Frontend: 200 ChatResponse
    end
```

### Component Interaction Overview

```mermaid
graph TB
    subgraph "Frontend Layer"
        Frontend[AEvalTrae React App]
    end

    subgraph "API Layer"
        FastAPI[FastAPI Server]
        CORS[CORS Middleware]
        Router[Chat Router]
    end

    subgraph "Service Layer"
        ChatSvc[ChatService Singleton]
        DataSvc[DataService]
    end

    subgraph "Agent Layer"
        Agent[EvaluationAgent]
        Client[ZhipuAI Client]
    end

    subgraph "Data Layer"
        JSON[(JSON Files)]
        Cache[Internal Cache]
    end

    subgraph "External Services"
        LLM[z.ai LLM API]
    end

    Frontend -->|HTTP POST| FastAPI
    FastAPI --> CORS
    CORS --> Router
    Router --> ChatSvc
    ChatSvc --> DataSvc
    DataSvc --> JSON
    DataSvc --> Cache
    ChatSvc --> Agent
    Agent --> Client
    Client --> LLM

    style Frontend fill:#e1f5fe
    style FastAPI fill:#c8e6c9
    style ChatSvc fill:#fff9c4
    style Agent fill:#f3e5f5
    style LLM fill:#ffccbc
    style JSON fill:#eceff1
```

## API Endpoints

### Health Check
```
GET /health
```

Returns server health status.

### Chat
```
POST /api/chat
Content-Type: application/json

{
  "message": "Test my RAG agent for safety"
}
```

Returns AI response with evaluation configuration recommendation.

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_agents.py -v
```

## Frontend Integration

The frontend (AEvalTrae) connects to this backend via the `/api/chat` endpoint.

To run the full stack:

1. Start the backend:
   ```bash
   cd aeval-backend/backend
   source venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Start the frontend (in another terminal):
   ```bash
   cd AEvalTrae
   npm install
   npm run dev
   ```

3. Open `http://localhost:5173` in your browser

## Configuration

Environment variables (see `.env.example`):

| Variable | Description | Default |
|----------|-------------|---------|
| `ZAI_API_KEY` | z.ai API key | *Required* |
| `ZAI_BASE_URL` | z.ai API base URL | `https://api.z.ai/v1` |
| `ZAI_MODEL` | Model to use | `gpt-4o-mini` |
| `API_HOST` | API host | `0.0.0.0` |
| `API_PORT` | API port | `8000` |
| `AGENT_TEMPERATURE` | LLM temperature | `0.7` |
| `AGENT_MAX_TOKENS` | Max tokens for LLM response | `2000` |
| `DATA_DIR` | Data directory | `data` |

## Development

### Code Style

The project uses:
- **Black** for code formatting
- **Ruff** for linting

Format code:
```bash
black app/ tests/
```

Lint code:
```bash
ruff check app/ tests/
```

### Adding New Data

To add new datasets, metrics, scenarios, or agents, edit the JSON files in the `data/` directory:

- `data/datasets.json` - Evaluation datasets
- `data/metrics.json` - Evaluation metrics
- `data/scenarios.json` - Evaluation scenarios
- `data/agents.json` - AI agent configurations

The backend automatically loads these files on startup.

## Troubleshooting

### "Module not found" errors
Make sure the virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Connection refused" from frontend
1. Check that the backend is running on port 8000
2. Verify `VITE_API_URL` in frontend `.env.local` matches backend URL
3. Check browser console for CORS errors

### API key errors
1. Verify `ZAI_API_KEY` is set in `.env` file
2. Check that the API key is valid and active
3. Ensure `ZAI_BASE_URL` is correct for your provider

## License

MIT
