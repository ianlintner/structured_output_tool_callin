# Quick Start

Get up and running with Pet Paradise Shop in minutes!

## Automated Start (Recommended)

The easiest way to start the system:

```bash
./start.sh
```

This script will:

1. ✓ Check for `.env` configuration
2. ✓ Create virtual environment (if needed)
3. ✓ Install dependencies
4. ✓ Check MongoDB connectivity
5. ✓ Start the API server
6. ✓ Start the Chainlit chat interface

## Manual Start

### Terminal 1: Start the API Server

```bash
python api.py
```

You should see:

```
✓ Connected to MongoDB: petshop
✓ Initialized database with 10 sample pets
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Start the Chat Interface

```bash
chainlit run app.py
```

You should see:

```
2024-12-24 - Chainlit - INFO - Your app is available at http://localhost:8001
```

## Access the Application

- **Chat Interface**: [http://localhost:8001](http://localhost:8001)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

## First Conversation

Once the chat interface is open, try these example conversations:

### Browse Pets

```
You: Show me all available pets
```

The AI will use the `browse_pets` tool to fetch the inventory.

### Filter by Type

```
You: What dogs do you have?
```

### Filter by Price

```
You: Show me pets under $500
```

### Place an Order

```
You: I'd like to order the Golden Retriever puppy

[AI will ask for your information]

You: My name is John Doe, email john@example.com, 
     phone 555-1234, address 123 Main St, City, ST 12345
```

The AI will use the `place_order` tool and provide an order ID.

### Check Order Status

```
You: What's the status of order ORD-ABC12345?
```

## Using the REST API Directly

### Browse Pets

```bash
# Get all pets
curl http://localhost:8000/pets

# Filter by type
curl "http://localhost:8000/pets?pet_type=dog"

# Filter by price
curl "http://localhost:8000/pets?max_price=500"
```

### Create an Order

```bash
curl -X POST http://localhost:8000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_phone": "555-1234",
    "delivery_address": "123 Main St, City, ST 12345",
    "pet_ids": ["pet001"]
  }'
```

### Check Order Status

```bash
curl http://localhost:8000/orders/ORD-ABC12345/status
```

## Docker Deployment

For a containerized deployment:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at the same ports.

## Verify Everything Works

### 1. Check API Health

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

### 2. Run Demo

```bash
python demo.py
```

This will show examples of structured outputs and tool calling.

### 3. Run Tests

```bash
python test_validation.py
```

All tests should pass.

## Common Issues

### Port Already in Use

If port 8000 or 8001 is in use, edit `.env`:

```env
API_PORT=8001  # Change to available port
```

For Chainlit, it automatically finds the next available port.

### MongoDB Not Connected

Ensure MongoDB is running:

```bash
# Check if MongoDB is running
mongod --version

# Start MongoDB
mongod

# Or with Docker
docker run -d -p 27017:27017 mongo:latest
```

### Azure OpenAI Errors

Verify your `.env` configuration:

```bash
cat .env | grep AZURE
```

Make sure all Azure OpenAI variables are set correctly.

## Next Steps

- Explore the [Chat Interface Guide](../user-guide/chat-interface.md)
- Read about [Configuration Options](configuration.md)
- Learn about the [Architecture](../architecture/overview.md)
