#!/bin/bash

# Development startup script
# Starts both backend and frontend in separate terminals

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Starting development servers...${NC}"
echo ""

# Check if we're in the project root
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Function to start backend
start_backend() {
    echo -e "${GREEN}📦 Starting backend on http://localhost:8000${NC}"
    cd backend
    if [ ! -d ".venv" ] && [ ! -f "poetry.lock" ]; then
        echo "Installing backend dependencies..."
        poetry install
    fi
    poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

# Function to start frontend
start_frontend() {
    echo -e "${GREEN}🎨 Starting frontend on http://localhost:5173${NC}"
    cd frontend
    if [ ! -d "node_modules" ]; then
        echo "Installing frontend dependencies..."
        npm install
    fi
    npm run dev
}

# Check for available terminal emulators
if command -v gnome-terminal &> /dev/null; then
    # GNOME Terminal
    gnome-terminal -- bash -c "cd $(pwd) && source start-dev.sh && start_backend; exec bash" &
    sleep 2
    gnome-terminal -- bash -c "cd $(pwd) && source start-dev.sh && start_frontend; exec bash" &
elif command -v xterm &> /dev/null; then
    # xterm
    xterm -e "cd $(pwd) && bash -c 'source start-dev.sh && start_backend; exec bash'" &
    sleep 2
    xterm -e "cd $(pwd) && bash -c 'source start-dev.sh && start_frontend; exec bash'" &
else
    echo ""
    echo -e "${YELLOW}⚠️  Could not detect terminal emulator${NC}"
    echo ""
    echo "Please run these commands in separate terminals:"
    echo ""
    echo -e "${GREEN}Terminal 1 - Backend:${NC}"
    echo "  cd backend"
    echo "  poetry shell"
    echo "  uvicorn app.main:app --reload"
    echo ""
    echo -e "${GREEN}Terminal 2 - Frontend:${NC}"
    echo "  cd frontend"
    echo "  npm run dev"
    echo ""
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Development servers starting!${NC}"
echo ""
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""

