#!/bin/bash
# Startup script for Pet Paradise Shop

echo "🐾 Starting Pet Paradise Shop..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env with your Azure OpenAI credentials and MongoDB URI"
    echo "Then run this script again."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Check MongoDB connection
echo "🔍 Checking MongoDB connection..."
if ! command -v mongod &> /dev/null; then
    echo "⚠️  MongoDB not found. Make sure MongoDB is running or update MONGODB_URI in .env"
fi

# Start API in background
echo "🚀 Starting API server..."
python api.py > api.log 2>&1 &
API_PID=$!
echo "API server started (PID: $API_PID)"

# Wait for API to be ready
echo "⏳ Waiting for API to be ready..."
sleep 5

# Check API health
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ API is healthy"
else
    echo "⚠️  API health check failed"
fi

# Start Chainlit
echo "🚀 Starting Chainlit chat interface..."
echo "📱 Chat will be available at http://localhost:8001"
echo "📚 API docs available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

chainlit run app.py

# Cleanup on exit
echo ""
echo "🛑 Stopping services..."
kill $API_PID
echo "✅ All services stopped"
