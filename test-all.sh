#!/bin/bash

# Test script for running all tests in the project

set -e  # Exit on error

echo "🧪 Running all tests..."
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend tests
echo -e "${YELLOW}📦 Running backend tests...${NC}"
cd backend
if poetry run pytest -v; then
    echo -e "${GREEN}✅ Backend tests passed!${NC}"
else
    echo -e "${RED}❌ Backend tests failed!${NC}"
    exit 1
fi
cd ..

echo ""

# Frontend tests
echo -e "${YELLOW}🎨 Running frontend tests...${NC}"
cd frontend
if npm test -- --run; then
    echo -e "${GREEN}✅ Frontend tests passed!${NC}"
else
    echo -e "${RED}❌ Frontend tests failed!${NC}"
    exit 1
fi
cd ..

echo ""
echo -e "${GREEN}🎉 All tests passed!${NC}"

