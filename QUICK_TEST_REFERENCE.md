# Quick Test Reference

## 🚀 Quick Start

### Backend Tests
```bash
cd backend
poetry install  # First time only
poetry run pytest
```

### Frontend Tests
```bash
cd frontend
npm install  # First time only
npm test
```

### Run All Tests
```bash
./test-all.sh
```

## 📋 Test Commands Cheat Sheet

### Backend
| Command | Description |
|---------|-------------|
| `poetry run pytest` | Run all tests |
| `poetry run pytest -v` | Verbose output |
| `poetry run pytest tests/test_health.py` | Run specific test file |
| `poetry run pytest --cov=app` | With coverage |

### Frontend
| Command | Description |
|---------|-------------|
| `npm test` | Run tests in watch mode |
| `npm test -- --run` | Run tests once |
| `npm run test:ui` | Open test UI |
| `npm run test:coverage` | With coverage |

### Integration
| Command | Description |
|---------|-------------|
| `docker-compose up` | Start all services |
| `curl http://localhost:8000/health` | Test backend health |
| `curl -X POST http://localhost:8000/api/predict/ -H "Content-Type: application/json" -d '{"inputs": [1,2,3,4]}'` | Test prediction |

## 🎯 What to Test

### ✅ Backend
- [x] Health endpoint (`/health`)
- [x] Prediction endpoint (`/api/predict/`)
- [x] Models listing (`/api/models/`)
- [x] Model info (`/api/models/{name}`)

### ✅ Frontend
- [x] Component rendering
- [x] User input handling
- [x] API integration
- [x] Result display

## 📚 Full Documentation

See [TESTING_GUIDE.md](./TESTING_GUIDE.md) for comprehensive testing documentation.
