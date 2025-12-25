# Installation

This guide will walk you through installing and setting up the Pet Paradise Shop system.

## Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8 or higher**
- **MongoDB** (local installation or MongoDB Atlas)
- **Azure OpenAI account** with API access
- **Git** for cloning the repository

## System Requirements

- **OS**: Linux, macOS, or Windows with WSL
- **RAM**: Minimum 4GB
- **Disk Space**: At least 1GB free

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/ianlintner/structured_output_tool_callin.git
cd structured_output_tool_callin
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages:

- `chainlit` - Chat interface
- `openai` - Azure OpenAI client
- `pydantic` - Data validation
- `fastapi` - REST API framework
- `uvicorn` - ASGI server
- `motor` - Async MongoDB driver
- `httpx` - Async HTTP client
- `python-dotenv` - Environment management

### 4. Set Up MongoDB

#### Option A: Local MongoDB

Install MongoDB locally:

```bash
# Ubuntu/Debian
sudo apt-get install mongodb

# macOS (using Homebrew)
brew install mongodb-community

# Start MongoDB
mongod
```

#### Option B: Docker MongoDB

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

#### Option C: MongoDB Atlas

1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Get your connection string
4. Update `MONGODB_URI` in your `.env` file

### 5. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=petshop

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### 6. Verify Installation

Run the validation tests:

```bash
python test_validation.py
```

You should see:

```
==================================================
✓ All validation tests passed!
==================================================
```

## Next Steps

- Continue to [Quick Start](quickstart.md) to run the system
- Read [Configuration](configuration.md) for advanced setup options
- Explore the [User Guide](../user-guide/chat-interface.md) to learn how to use the system

## Troubleshooting

### Import Errors

If you see import errors, make sure you activated your virtual environment:

```bash
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### MongoDB Connection Issues

- Verify MongoDB is running: `mongod --version`
- Check the connection string in `.env`
- For Atlas, verify IP whitelist and credentials

### Azure OpenAI Errors

- Verify your API key is correct
- Check the endpoint URL format
- Ensure the deployment name matches your Azure resource
- Confirm API version compatibility

## Optional: Development Dependencies

For development and testing:

```bash
# Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy mkdocs mkdocs-material
```
