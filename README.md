# Pet Paradise Shop - Chainlit Chat Assistant

A complete pet shop ordering and support system built with Chainlit, Azure OpenAI, structured outputs, and MongoDB. Features an AI-powered chat assistant that helps customers browse pets, place orders, and track their purchases.

## 🌟 Features

- **🤖 AI Chat Assistant**: Intelligent Chainlit-based chat interface powered by Azure OpenAI
- **🛠️ Structured Tool Calling**: Type-safe tool calling with Pydantic validation
- **🐾 Pet Inventory**: Browse dogs, cats, birds, fish, rabbits, and hamsters
- **🛒 Order Management**: Complete order placement and tracking system
- **📦 REST API**: FastAPI-based backend with MongoDB database
- **✅ Structured Outputs**: Azure OpenAI structured outputs with strict validation
- **📚 OpenAPI Documentation**: Interactive API docs at `/docs` and OpenAPI spec at `/openapi.json`
- **📊 Observability**: OpenTelemetry tracing, Prometheus metrics, Jaeger UI

## 🏗️ Architecture

### Components

1. **Chainlit Chat App** (`app.py`): User-facing chat interface
2. **REST API** (`api.py`): FastAPI service for pet shop operations
3. **Tool Calling** (`tools.py`): AI agent tools for browsing, ordering, and tracking
4. **Data Models** (`models.py`): Pydantic models for structured validation
5. **Database** (`database.py`): MongoDB connection and data management

### Technology Stack

- **Frontend**: Chainlit
- **AI**: Azure OpenAI (GPT-4) with structured outputs
- **Backend**: FastAPI
- **Database**: MongoDB
- **Validation**: Pydantic v2
- **Language**: Python 3.8+

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB (local or cloud instance)
- Azure OpenAI account with API access
- Azure OpenAI deployment (GPT-4 recommended)

## 🚀 Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/ianlintner/structured_output_tool_callin.git
cd structured_output_tool_callin
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file from the example:

```bash
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

### 3. Start MongoDB

**Local MongoDB:**
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or start your local MongoDB service
mongod
```

**MongoDB Atlas:**
- Update `MONGODB_URI` in `.env` with your Atlas connection string

### 4. Start the API Server

In one terminal:

```bash
python api.py
```

The API will be available at `http://localhost:8000`

- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 5. Start the Chainlit Chat App

In another terminal:

```bash
chainlit run app.py
```

The chat interface will open at `http://localhost:8001`

## 💬 Using the Chat Assistant

### Browse Pets

```
User: "Show me all available dogs"
User: "What cats do you have under $700?"
User: "Show me young pets (under 6 months)"
```

### Place Orders

```
User: "I'd like to order the Golden Retriever"
Assistant: [Collects customer information]
User: [Provides name, email, phone, address]
Assistant: [Places order and provides order ID]
```

### Check Order Status

```
User: "What's the status of my order ORD-12345678?"
Assistant: [Shows order status and details]
```

## 🔧 API Endpoints

The API provides comprehensive OpenAPI documentation:

- **Interactive Docs (Swagger UI)**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **OpenAPI JSON Spec**: http://localhost:8000/openapi.json

### GET /pets
Browse available pets with optional filters.

**Query Parameters:**
- `pet_type`: Filter by type (dog, cat, bird, fish, rabbit, hamster)
- `max_price`: Maximum price
- `min_age_months`: Minimum age in months
- `max_age_months`: Maximum age in months
- `available_only`: Show only available pets (default: true)

**Example:**
```bash
curl "http://localhost:8000/pets?pet_type=dog&max_price=1000"
```

### POST /orders
Create a new order.

**Request Body:**
```json
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "555-0123",
  "delivery_address": "123 Main St, City, ST 12345",
  "pet_ids": ["pet001", "pet002"]
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"John Doe","customer_email":"john@example.com","customer_phone":"555-0123","delivery_address":"123 Main St","pet_ids":["pet001"]}'
```

### GET /orders/{order_id}/status
Check order status.

**Example:**
```bash
curl http://localhost:8000/orders/ORD-12345678/status
```

## 🛠️ Tool Calling

The chat assistant uses three main tools:

### 1. browse_pets
Browse available pets with filters.

**Parameters:**
- `pet_type` (optional): Type of pet
- `max_price` (optional): Maximum price
- `min_age_months` (optional): Minimum age
- `max_age_months` (optional): Maximum age

### 2. place_order
Place an order for pets.

**Parameters:**
- `customer_name`: Customer's full name
- `customer_email`: Email address
- `customer_phone`: Phone number
- `delivery_address`: Full delivery address
- `pet_ids`: List of pet IDs to order

### 3. check_order_status
Check the status of an order.

**Parameters:**
- `order_id`: Order ID to check

## 📊 Data Models

### Pet
```python
{
  "id": "pet001",
  "name": "Golden Retriever Puppy",
  "type": "dog",
  "description": "Friendly and energetic...",
  "price": 1200.00,
  "age_months": 3,
  "available": true,
  "image_url": "https://..."
}
```

### Order
```python
{
  "id": "ORD-12345678",
  "customer": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-0123",
    "address": "123 Main St..."
  },
  "items": [...],
  "total_amount": 1200.00,
  "status": "pending",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## 🧪 Testing

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Get all pets
curl http://localhost:8000/pets

# Get specific pet
curl http://localhost:8000/pets/pet001
```

### Test the Chat Interface

1. Open http://localhost:8001
2. Try these conversations:
   - "Show me all available pets"
   - "I want to see dogs under $1000"
   - "I'd like to order pet001"
   - "Check order status ORD-XXXXXXXX"

## 🔒 Security Notes

- Never commit your `.env` file
- Rotate API keys regularly
- Use environment variables for all secrets
- Enable authentication in production
- Use HTTPS in production
- Validate all user inputs

## 📝 Sample Data

The system initializes with 10 sample pets:
- 3 Dogs (Golden Retriever, Beagle, German Shepherd)
- 2 Cats (British Shorthair, Siamese)
- 2 Birds (Cockatiel, Parakeets)
- 1 Fish (Betta)
- 1 Rabbit (Holland Lop)
- 1 Hamster (Syrian)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `mongod --version`
- Check connection string in `.env`
- For Atlas, verify IP whitelist and credentials

### Azure OpenAI Issues
- Verify API key and endpoint in `.env`
- Check deployment name matches your Azure OpenAI deployment
- Ensure API version is compatible

### Port Already in Use
- Change `API_PORT` in `.env` for the API
- Chainlit uses port 8001 by default (configurable)

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation at `/docs` endpoint
- Review API documentation at `http://localhost:8000/docs`