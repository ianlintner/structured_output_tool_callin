# Configuration

Configure Pet Paradise Shop for your environment and requirements.

## Environment Variables

All configuration is managed through environment variables in the `.env` file.

### Azure OpenAI Configuration

```env
# Required: Your Azure OpenAI API key
AZURE_OPENAI_API_KEY=your_azure_openai_api_key

# Required: Your Azure OpenAI endpoint
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Required: Your deployment name (model)
AZURE_OPENAI_DEPLOYMENT=gpt-4

# Required: API version
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

#### Getting Azure OpenAI Credentials

1. Log in to [Azure Portal](https://portal.azure.com/)
2. Navigate to your Azure OpenAI resource
3. Go to "Keys and Endpoint"
4. Copy your API key and endpoint
5. Note your deployment name from the "Deployments" section

### MongoDB Configuration

```env
# MongoDB connection URI
MONGODB_URI=mongodb://localhost:27017

# Database name
MONGODB_DATABASE=petshop
```

#### Connection String Examples

**Local MongoDB:**
```env
MONGODB_URI=mongodb://localhost:27017
```

**MongoDB with Authentication:**
```env
MONGODB_URI=mongodb://username:password@localhost:27017
```

**MongoDB Atlas:**
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

**Docker MongoDB:**
```env
MONGODB_URI=mongodb://mongodb:27017
```

### API Configuration

```env
# Host to bind the API server
API_HOST=0.0.0.0

# Port for the API server
API_PORT=8000

# Base URL for API (used by tools)
API_BASE_URL=http://localhost:8000
```

## Chainlit Configuration

Chainlit configuration is stored in `.chainlit` file.

### Key Settings

```toml
[project]
# Enable/disable telemetry
enable_telemetry = false

# Session timeout (seconds)
session_timeout = 3600

[UI]
# App name displayed in UI
name = "Pet Paradise Shop"

# App description
description = "Pet shop ordering and support chat assistant"

# Collapse large content
default_collapse_content = true
```

### Customization

To customize the UI theme, edit the `.chainlit` file:

```toml
[UI.theme.light]
background = "#FAFAFA"
paper = "#FFFFFF"

[UI.theme.light.primary]
main = "#F80061"
dark = "#980039"
light = "#FFE7EB"
```

## Advanced Configuration

### API Server Options

For production deployments, you can configure Uvicorn options:

```python
# In api.py
uvicorn.run(
    app,
    host=host,
    port=port,
    workers=4,  # Number of worker processes
    log_level="info",
    access_log=True,
    ssl_keyfile="path/to/key.pem",  # For HTTPS
    ssl_certfile="path/to/cert.pem"
)
```

### MongoDB Indexes

For better performance, create indexes:

```python
# Add to database.py initialization
await db.db.pets.create_index([("type", 1)])
await db.db.pets.create_index([("price", 1)])
await db.db.pets.create_index([("available", 1)])
await db.db.orders.create_index([("created_at", -1)])
```

### Tool Configuration

Customize tool behavior in `tools.py`:

```python
# Change API base URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Adjust HTTP timeout
async with httpx.AsyncClient(timeout=30.0) as client:
    # Tool implementation
```

## Security Configuration

### Production Recommendations

1. **Use HTTPS**: Configure SSL certificates for API
2. **Restrict CORS**: Limit allowed origins in `api.py`
3. **Authentication**: Add API key or OAuth
4. **Rate Limiting**: Implement rate limits
5. **Secret Management**: Use Azure Key Vault or similar

### CORS Configuration

Edit `api.py` to restrict CORS:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Limit methods
    allow_headers=["*"],
)
```

### Environment-Specific Configuration

Use different `.env` files for different environments:

```bash
# Development
cp .env.development .env

# Staging
cp .env.staging .env

# Production
cp .env.production .env
```

## Docker Configuration

### Docker Compose Environment

Create `docker-compose.override.yml` for local overrides:

```yaml
version: '3.8'

services:
  api:
    environment:
      - DEBUG=true
      - LOG_LEVEL=debug
  
  chat:
    ports:
      - "8002:8001"  # Use different port
```

### Build Arguments

Customize Docker builds:

```dockerfile
# In Dockerfile.api
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim
```

Build with custom arguments:

```bash
docker build --build-arg PYTHON_VERSION=3.12 -f Dockerfile.api .
```

## Logging Configuration

### Application Logging

Configure logging in your application:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### API Access Logs

Uvicorn provides access logging:

```bash
python api.py --log-config logging.yaml
```

## Performance Tuning

### Connection Pooling

MongoDB connection pool settings:

```python
client = AsyncIOMotorClient(
    mongodb_uri,
    maxPoolSize=50,
    minPoolSize=10,
    serverSelectionTimeoutMS=5000
)
```

### API Workers

Scale API with multiple workers:

```bash
uvicorn api:app --workers 4 --host 0.0.0.0 --port 8000
```

### Caching

Add caching for frequently accessed data:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
async def get_pet_by_id(pet_id: str):
    # Implementation
```

## Monitoring Configuration

### Health Checks

The `/health` endpoint provides system status:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Metrics

Consider adding Prometheus metrics:

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

## Next Steps

- Start the system with [Quick Start](quickstart.md)
- Explore [Architecture](../architecture/overview.md)
