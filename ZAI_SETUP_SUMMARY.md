# z.ai Backend Setup Summary

## Configuration Completed ✅

The backend has been successfully configured to use z.ai's API with your credentials.

## What Was Changed

### 1. Dependencies Updated
- **requirements.txt**: Changed from `openai` to `zhipuai>=2.0.0`
- Installed `zhipuai` package (version 2.1.5.20250825)

### 2. Agent Code Updated
- **app/agents/evaluation_agent.py**:
  - Changed import from `openai` to `zhipuai`
  - Using `ZhipuAI` client class
  - Using `chat.asyncCompletions.create()` API

### 3. Configuration Updated
- **app/config.py**:
  - Removed `zai_base_url` (not needed for zhipuai SDK)
  - Changed default model to `glm-4.7`

### 4. Environment Configured
- **.env file created** with your API key:
  - API Key: `your_zai_api_key_here` (Get from https://open.bigmodel.cn/usercenter/apikeys)
  - Model: `glm-4.7`
  - Temperature: `0.7`
  - Max Tokens: `2000`

## Test Results

```
✓ Settings loaded (model: glm-4.7)
✓ All models imported
✓ All services imported
✓ Agent imported
✓ FastAPI app imported
✓ Loaded 10 datasets
✓ Loaded 20 metrics
✓ Loaded 5 scenarios
✓ Loaded 3 agents
✓ Agent initialized with API key
```

## How to Start the Backend

### Option 1: Quick Start
```bash
cd aeval-backend/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Using the setup script
```bash
cd aeval-backend/backend
./setup.sh
```

## Access Points

- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs
- **Chat Endpoint**: http://localhost:8000/api/chat

## API Usage Example

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test my RAG agent for safety"}'
```

## Frontend Integration

The frontend is already configured to connect to this backend at:
- **Frontend**: `../AEvalTrae`
- **API URL**: `http://localhost:8000/api` (set in `.env.local`)

### Start Both Services

**Terminal 1 - Backend:**
```bash
cd aeval-backend/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd ../AEvalTrae
npm run dev
```

**Then open:** http://localhost:5173

## z.ai API Details

- **Model**: `glm-4.7`
- **Client**: `zhipuai.ZhipuAI`
- **Method**: `chat.asyncCompletions.create()`
- **API Key format**: `id.secret`

## Important Notes

1. **API Key Security**: Your API key is stored in `.env` which is in `.gitignore`
2. **Model Selection**: Using `glm-4.7` - can be changed in `.env` if needed
3. **Temperature**: Set to `0.7` for balanced creativity
4. **Max Tokens**: Set to `2000` for responses

## Troubleshooting

### If server doesn't start:
```bash
# Check if port 8000 is free
lsof -i :8000

# Kill any process using port 8000
kill -9 <PID>

# Try starting again
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### If API calls fail:
1. Check API key is correct in `.env`
2. Verify internet connectivity
3. Check z.ai service status

### Verify setup anytime:
```bash
python3 test_setup.py
```

## Files Modified

1. `requirements.txt` - Updated to use zhipuai
2. `app/config.py` - Updated model and removed base_url
3. `app/agents/evaluation_agent.py` - Updated to use ZhipuAI client
4. `.env` - Created with your API key
5. `.env.example` - Updated template
6. `setup.sh` - Updated install command
7. `test_setup.py` - Created verification script

## Next Steps

1. Start the backend server
2. Start the frontend development server
3. Open the frontend in your browser
4. Test the chat functionality with real AI responses from z.ai!
