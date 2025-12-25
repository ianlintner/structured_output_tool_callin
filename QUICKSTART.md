# Pet Paradise Shop - Quick Reference Guide

## 🚀 Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Start everything (automated)
./start.sh

# OR start manually:
# Terminal 1: Start API
python api.py

# Terminal 2: Start Chat
chainlit run app.py
```

## 📁 Project Structure

```
.
├── app.py              # Chainlit chat application (main entry point)
├── api.py              # FastAPI REST API server
├── models.py           # Pydantic models for structured outputs
├── tools.py            # Tool calling functions for AI agent
├── database.py         # MongoDB connection and initialization
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── start.sh           # Automated startup script
├── docker-compose.yml  # Docker deployment configuration
└── README.md          # Full documentation

Demo & Testing:
├── demo.py            # System demonstration
├── test_validation.py # Validation tests
```

## 🔑 Key Components

### 1. Pydantic Models (models.py)

**Core Data Models:**
- `Pet` - Pet inventory model
- `Order` - Order management model
- `CustomerInfo` - Customer details
- `OrderItem` - Individual order items

**Tool Input/Output Models:**
- `BrowsePetsInput` - Parameters for browsing pets
- `PlaceOrderInput` - Parameters for placing orders
- `CheckOrderStatusInput` - Parameters for status checks
- `BrowsePetsOutput` - Structured browse results
- `PlaceOrderOutput` - Structured order confirmation
- `OrderStatusResponse` - Structured status info

### 2. REST API (api.py)

**Endpoints:**
```
GET  /                 - API information
GET  /health           - Health check
GET  /pets             - List pets (with filters)
GET  /pets/{id}        - Get specific pet
POST /orders           - Create order
GET  /orders/{id}      - Get order details
GET  /orders/{id}/status - Get order status
PUT  /orders/{id}/status - Update order status
```

### 3. Tool Calling (tools.py)

**Available Tools:**
- `browse_pets` - Browse pet inventory
- `place_order` - Place new order
- `check_order_status` - Check order status

**Tool Definitions:**
- JSON schemas for Azure OpenAI
- Type-safe parameter validation
- Structured response formats

### 4. Chat App (app.py)

**Features:**
- Chainlit-based interface
- Azure OpenAI integration
- Automatic tool calling
- Conversation history
- Error handling

## 💻 Usage Examples

### Browse Pets (API)

```bash
# Get all pets
curl http://localhost:8000/pets

# Filter by type
curl "http://localhost:8000/pets?pet_type=dog"

# Filter by price
curl "http://localhost:8000/pets?max_price=500"

# Multiple filters
curl "http://localhost:8000/pets?pet_type=cat&max_price=700&min_age_months=2"
```

### Place Order (API)

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

### Chat Examples

**Browse pets:**
```
User: Show me all available dogs
User: What cats do you have under $700?
User: Show me young pets under 6 months old
```

**Place order:**
```
User: I'd like to order the Golden Retriever
[AI collects customer info]
User: My name is Sarah, email sarah@email.com...
[AI places order]
```

**Check status:**
```
User: What's the status of my order ORD-ABC12345?
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# Azure OpenAI (Required)
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=petshop

# API
API_HOST=0.0.0.0
API_PORT=8000
```

## 🐳 Docker Deployment

```bash
# Start all services with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🧪 Testing

```bash
# Run validation tests
python test_validation.py

# Run demo
python demo.py

# Test API health
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs
```

## 📊 Sample Data

System includes 10 sample pets:
- **Dogs**: Golden Retriever ($1200), Beagle ($950), German Shepherd ($1500)
- **Cats**: British Shorthair ($800), Siamese ($650)
- **Birds**: Cockatiel ($150), Parakeet Pair ($80)
- **Fish**: Betta ($25)
- **Rabbit**: Holland Lop ($300)
- **Hamster**: Syrian ($45)

## 🔐 Security Best Practices

1. **Never commit .env file**
2. **Rotate API keys regularly**
3. **Use HTTPS in production**
4. **Enable authentication**
5. **Validate all inputs**
6. **Sanitize user data**
7. **Use environment variables**
8. **Keep dependencies updated**

## 📚 Additional Resources

- [Chainlit Documentation](https://docs.chainlit.io/)
- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)

## 🆘 Common Issues

**MongoDB not connecting:**
```bash
# Start MongoDB with Docker
docker run -d -p 27017:27017 mongo:latest

# Or check if MongoDB is running
systemctl status mongod
```

**Port already in use:**
```bash
# Change API_PORT in .env
API_PORT=8001
```

**Azure OpenAI errors:**
- Verify API key is correct
- Check endpoint URL format
- Ensure deployment name matches
- Verify API version compatibility

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 💡 Tips

1. **Use the demo**: Run `python demo.py` to understand the system
2. **Check API docs**: Visit `/docs` for interactive API documentation
3. **Monitor logs**: Watch API logs for debugging
4. **Start simple**: Test API endpoints before using chat
5. **Use filters**: Take advantage of pet filtering for better UX

## 🎯 Next Steps

1. Configure Azure OpenAI credentials
2. Start MongoDB
3. Run the demo to verify setup
4. Test API endpoints
5. Launch chat interface
6. Try example conversations
7. Customize for your needs
