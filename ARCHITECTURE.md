# Pet Paradise Shop - System Architecture

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                          │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Chainlit Chat Interface (app.py)             │  │
│  │  • Rich UI with markdown support                          │  │
│  │  • Real-time chat interaction                             │  │
│  │  • Message history management                             │  │
│  │  • File upload support                                    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      AI ORCHESTRATION LAYER                      │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │            Azure OpenAI (GPT-4 with Tools)                │  │
│  │  • Natural language understanding                         │  │
│  │  • Structured output generation                           │  │
│  │  • Tool calling decisions                                 │  │
│  │  • Response synthesis                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      TOOL CALLING LAYER                          │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │  browse_pets     │  │  place_order     │  │ check_order  │  │
│  │  (tools.py)      │  │  (tools.py)      │  │ (tools.py)   │  │
│  │                  │  │                  │  │              │  │
│  │ • Filter pets    │  │ • Validate data  │  │ • Get status │  │
│  │ • Format results │  │ • Create order   │  │ • Track info │  │
│  │ • HTTP calls     │  │ • Confirm order  │  │ • Details    │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│                                                                   │
│  Tool Definitions (JSON Schema):                                 │
│  • Type-safe parameters                                          │
│  • Structured inputs/outputs                                     │
│  • Pydantic validation                                           │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      VALIDATION LAYER                            │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │           Pydantic Models (models.py)                     │  │
│  │                                                           │  │
│  │  Data Models:          Tool Models:                      │  │
│  │  • Pet                 • BrowsePetsInput                 │  │
│  │  • Order               • PlaceOrderInput                 │  │
│  │  • CustomerInfo        • CheckOrderStatusInput           │  │
│  │  • OrderItem           • BrowsePetsOutput                │  │
│  │                        • PlaceOrderOutput                │  │
│  │                        • OrderStatusResponse             │  │
│  │                                                           │  │
│  │  Features:                                                │  │
│  │  ✓ Type safety with enums (PetType, OrderStatus)        │  │
│  │  ✓ Automatic validation (price > 0, age >= 0)           │  │
│  │  ✓ JSON serialization/deserialization                   │  │
│  │  ✓ Auto-generated schemas                               │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      REST API LAYER                              │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              FastAPI Server (api.py)                      │  │
│  │                                                           │  │
│  │  Endpoints:                                               │  │
│  │  GET  /health              - Health check                │  │
│  │  GET  /pets                - List pets (with filters)    │  │
│  │  GET  /pets/{id}           - Get specific pet            │  │
│  │  POST /orders              - Create new order            │  │
│  │  GET  /orders/{id}         - Get order details           │  │
│  │  GET  /orders/{id}/status  - Get order status            │  │
│  │  PUT  /orders/{id}/status  - Update order status         │  │
│  │                                                           │  │
│  │  Features:                                                │  │
│  │  ✓ Automatic request/response validation                │  │
│  │  ✓ OpenAPI/Swagger docs                                  │  │
│  │  ✓ CORS support                                          │  │
│  │  ✓ Async operations                                      │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      DATA ACCESS LAYER                           │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │          MongoDB Connection (database.py)                 │  │
│  │                                                           │  │
│  │  Operations:                                              │  │
│  │  • Async connection management                           │  │
│  │  • Collection access (pets, orders)                      │  │
│  │  • Sample data initialization                            │  │
│  │  • Connection pooling                                    │  │
│  │                                                           │  │
│  │  Collections:                                             │  │
│  │  • pets      - Pet inventory (10 sample pets)            │  │
│  │  • orders    - Order history                             │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                              │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    MongoDB                                │  │
│  │                                                           │  │
│  │  Database: petshop                                        │  │
│  │  Collections:                                             │  │
│  │    • pets      - Pet inventory documents                 │  │
│  │    • orders    - Order documents                         │  │
│  │                                                           │  │
│  │  Features:                                                │  │
│  │  ✓ Document storage                                      │  │
│  │  ✓ Indexing for fast queries                            │  │
│  │  ✓ Flexible schema                                       │  │
│  │  ✓ Scalability                                           │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### Browse Pets Flow

```
1. User: "Show me dogs under $1000"
   ↓
2. Chainlit → Azure OpenAI (with message + tool definitions)
   ↓
3. Azure OpenAI decides to call browse_pets tool
   Parameters: {pet_type: "dog", max_price: 1000}
   ↓
4. Pydantic validates BrowsePetsInput
   ✓ pet_type is valid PetType enum
   ✓ max_price is positive number
   ↓
5. Tool calls FastAPI endpoint
   GET /pets?pet_type=dog&max_price=1000
   ↓
6. FastAPI validates query parameters with Pydantic
   ↓
7. MongoDB query executed
   Query: {type: "dog", price: {$lte: 1000}, available: true}
   ↓
8. Results validated with Pet model
   ↓
9. JSON response → Tool → Azure OpenAI
   ↓
10. Azure OpenAI generates natural response
    "I found 1 dog under $1000: Beagle for $950..."
    ↓
11. User sees friendly message in Chainlit
```

### Place Order Flow

```
1. User provides customer info and pet selection
   ↓
2. Azure OpenAI calls place_order tool
   Parameters: {customer_name, email, phone, address, pet_ids}
   ↓
3. Pydantic validates PlaceOrderInput
   ✓ All required fields present
   ✓ Email format valid
   ✓ Phone number provided
   ✓ Address min length met
   ↓
4. Tool calls FastAPI endpoint
   POST /orders with validated data
   ↓
5. FastAPI validates request body with PlaceOrderInput
   ↓
6. MongoDB operations:
   a. Verify pets exist and are available
   b. Create order document
   c. Mark pets as unavailable
   ↓
7. Order validated with Order model
   ↓
8. Response with order ID → Tool → Azure OpenAI
   ↓
9. Azure OpenAI generates confirmation
   "✓ Order confirmed! Order ID: ORD-ABC12345..."
   ↓
10. User receives order confirmation
```

## 🛡️ Validation & Type Safety

### Multi-Layer Validation

```
┌─────────────────────────────────────────┐
│  Layer 1: Pydantic Tool Input Models    │
│  Validates before tool execution        │
│  • Type checking                        │
│  • Required fields                      │
│  • Value constraints                    │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  Layer 2: FastAPI Request Validation    │
│  Validates HTTP requests                │
│  • Query parameters                     │
│  • Request body                         │
│  • Path parameters                      │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  Layer 3: Pydantic Data Models          │
│  Validates database operations          │
│  • Data integrity                       │
│  • Enum values                          │
│  • Field constraints                    │
└─────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────┐
│  Layer 4: MongoDB Schema                │
│  Database-level validation              │
│  • Document structure                   │
│  • Index constraints                    │
└─────────────────────────────────────────┘
```

## 🔧 Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **UI** | Chainlit | Chat interface with rich formatting |
| **AI** | Azure OpenAI (GPT-4) | Natural language processing + tool calling |
| **Validation** | Pydantic v2 | Structured outputs, type safety, validation |
| **API** | FastAPI | High-performance async REST API |
| **Database Driver** | Motor | Async MongoDB driver for Python |
| **Database** | MongoDB | NoSQL document storage |
| **HTTP Client** | httpx | Async HTTP for tool→API communication |
| **Environment** | python-dotenv | Configuration management |

## 📊 Key Features

### 1. Structured Outputs
- **Pydantic Models**: Type-safe data structures
- **Auto Validation**: Automatic data validation at every layer
- **JSON Schema**: Auto-generated for OpenAPI and tool definitions

### 2. Tool Calling
- **Type Safety**: Tools receive validated parameters
- **Error Handling**: Graceful failure with user-friendly messages
- **Async Operations**: Non-blocking tool execution

### 3. Conversation Management
- **Context Awareness**: Full conversation history
- **Multi-turn Dialogs**: Support for complex interactions
- **Tool Chaining**: Multiple tool calls in one conversation

### 4. Data Persistence
- **MongoDB**: Flexible document storage
- **Sample Data**: Pre-loaded pet inventory
- **Order Tracking**: Complete order history

## 🚀 Deployment Options

### Option 1: Local Development
```bash
./start.sh
```

### Option 2: Docker Compose
```bash
docker-compose up -d
```

### Option 3: Manual
```bash
# Terminal 1
python api.py

# Terminal 2
chainlit run app.py
```

## 🎯 Design Principles

1. **Type Safety First**: Pydantic ensures type correctness everywhere
2. **Separation of Concerns**: Clear layer boundaries
3. **Async All the Way**: Non-blocking I/O throughout
4. **Validation Everywhere**: Multiple validation layers
5. **DRY**: Shared Pydantic models across layers
6. **Testability**: Each component independently testable
7. **Scalability**: Async + MongoDB for horizontal scaling

## 📈 Scalability Considerations

- **Horizontal Scaling**: Stateless API can run multiple instances
- **Database**: MongoDB sharding for large datasets
- **Caching**: FastAPI + Redis for frequently accessed data
- **Load Balancing**: Nginx/HAProxy for distributing traffic
- **Async**: Non-blocking I/O for high concurrency
