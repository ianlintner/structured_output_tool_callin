# Pet Paradise Shop

![Pet Paradise](https://img.shields.io/badge/Status-Production%20Ready-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Azure](https://img.shields.io/badge/Azure-OpenAI-orange)

A complete pet shop ordering and support system built with **Chainlit**, **Azure OpenAI**, **structured outputs**, and **MongoDB**.

## 🌟 Features

- **🤖 AI Chat Assistant**: Intelligent Chainlit-based chat interface powered by Azure OpenAI
- **🛠️ Structured Tool Calling**: Type-safe tool calling with Pydantic validation
- **🐾 Pet Inventory**: Browse dogs, cats, birds, fish, rabbits, and hamsters
- **🛒 Order Management**: Complete order placement and tracking system
- **📦 REST API**: FastAPI-based backend with MongoDB database
- **✅ Structured Outputs**: Azure OpenAI structured outputs with strict validation

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/ianlintner/structured_output_tool_callin.git
cd structured_output_tool_callin

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Azure OpenAI credentials

# Start the system
./start.sh
```

Visit [http://localhost:8001](http://localhost:8001) to access the chat interface!

## 📚 Documentation Sections

### [Getting Started](getting-started/installation.md)
Learn how to install and configure the system.

### [User Guide](user-guide/chat-interface.md)
Discover how to use the chat interface and REST API.

### [Architecture](architecture/overview.md)
Understand the system design and components.

### [API Reference](api-reference/models.md)
Explore the detailed API documentation.

### [Deployment](deployment/docker.md)
Deploy the system using Docker or production environments.

### [Development](development/contributing.md)
Contribute to the project and run tests.

## 💡 Example Usage

**Browse pets:**
```
User: "Show me all available dogs"
User: "What cats do you have under $700?"
```

**Place order:**
```
User: "I'd like to order the Golden Retriever"
[AI collects customer information]
```

**Check status:**
```
User: "What's the status of my order ORD-ABC12345?"
```

## 🏗️ Architecture

```
User ↔ Chainlit Chat ↔ Azure OpenAI ↔ Tool Calling ↔ FastAPI ↔ MongoDB
```

The system uses structured outputs throughout, ensuring type safety and validation at every layer.

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| UI | Chainlit |
| AI | Azure OpenAI (GPT-4) |
| Validation | Pydantic v2 |
| API | FastAPI |
| Database | MongoDB |
| Language | Python 3.8+ |

## 📊 Sample Data

The system includes 10 pre-loaded pets:
- 3 Dogs (Golden Retriever, Beagle, German Shepherd)
- 2 Cats (British Shorthair, Siamese)
- 2 Birds (Cockatiel, Parakeets)
- 1 Fish (Betta)
- 1 Rabbit (Holland Lop)
- 1 Hamster (Syrian)

## 🔒 Security

- Environment variable management
- Multi-layer input validation
- Type-safe enums
- Error sanitization
- Async operations

## 📄 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guide](development/contributing.md) for details.
