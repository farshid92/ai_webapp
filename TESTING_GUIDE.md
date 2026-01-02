# Testing Guide

This guide covers how to test all components of the AI Webapp project, including backend, frontend, integration, and end-to-end testing.

## Table of Contents

1. [Backend Testing](#backend-testing)
2. [Frontend Testing](#frontend-testing)
3. [Integration Testing](#integration-testing)
4. [End-to-End Testing](#end-to-end-testing)
5. [Running All Tests](#running-all-tests)
6. [Test Coverage](#test-coverage)

---

## Backend Testing

The backend uses **pytest** for testing FastAPI endpoints and business logic.

### Setup

1. **Install dependencies** (if not already installed):
   ```bash
   cd backend
   poetry install
   ```

2. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

### Running Backend Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_health.py

# Run specific test
pytest tests/test_health.py::test_health_endpoint

# Run with coverage report
pytest --cov=app --cov-report=html

# View coverage report (opens in browser)
# Open htmlcov/index.html
```

### Test Structure

- `tests/conftest.py` - Shared fixtures and test configuration
- `tests/test_health.py` - Health check endpoint tests
- `tests/test_prediction.py` - Prediction API endpoint tests
- `tests/test_models.py` - Model management endpoint tests

### Writing New Backend Tests

1. Create test files in the `tests/` directory
2. Use the `client` fixture from `conftest.py` for API testing
3. Follow pytest conventions: `test_*.py` files, `test_*` functions

Example:
```python
def test_my_endpoint(client: TestClient):
    response = client.get("/api/my-endpoint")
    assert response.status_code == 200
```

---

## Frontend Testing

The frontend uses **Vitest** and **React Testing Library** for component testing.

### Setup

1. **Install dependencies** (if not already installed):
   ```bash
   cd frontend
   npm install
   ```

### Running Frontend Tests

```bash
# Run all tests in watch mode
npm test

# Run tests once
npm test -- --run

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

### Test Structure

- `src/test/setup.ts` - Test configuration and setup
- `src/test/App.test.tsx` - Main App component tests

### Writing New Frontend Tests

1. Create test files next to components: `Component.test.tsx`
2. Use React Testing Library for rendering and interactions
3. Mock API calls using `vi.mock()` or `global.fetch`

Example:
```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import MyComponent from './MyComponent'

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />)
    expect(screen.getByText('Hello')).toBeInTheDocument()
  })
})
```

---

## Integration Testing

Integration tests verify that backend and frontend work together correctly.

### Manual Integration Testing

1. **Start the backend**:
   ```bash
   cd backend
   poetry shell
   uvicorn app.main:app --reload
   ```
   Backend will be available at `http://localhost:8000`

2. **Start the frontend** (in another terminal):
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend will be available at `http://localhost:5173`

3. **Test the integration**:
   - Open `http://localhost:5173` in your browser
   - Enter values like `1, 2, 3, 4` in the input field
   - Click "Predict" button
   - Verify the prediction result appears

### API Testing with curl

Test backend endpoints directly:

```bash
# Health check
curl http://localhost:8000/health

# List models
curl http://localhost:8000/api/models/

# Get model info
curl http://localhost:8000/api/models/base

# Make a prediction
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"inputs": [1.0, 2.0, 3.0, 4.0], "model_name": "base"}'
```

### Using Docker Compose

1. **Start all services**:
   ```bash
   docker-compose up --build
   ```

2. **Access services**:
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8000`
   - Backend API docs: `http://localhost:8000/docs`

3. **Test endpoints**:
   ```bash
   # Health check
   curl http://localhost:8000/health

   # Prediction
   curl -X POST http://localhost:8000/api/predict/ \
     -H "Content-Type: application/json" \
     -d '{"inputs": [1.0, 2.0, 3.0, 4.0]}'
   ```

---

## End-to-End Testing

E2E tests verify the complete user workflow from frontend to backend.

### Manual E2E Testing Checklist

1. ✅ **Application loads**
   - Open frontend URL
   - Verify page loads without errors

2. ✅ **Health check**
   - Backend health endpoint responds
   - Frontend can communicate with backend

3. ✅ **Prediction flow**
   - Enter comma-separated numbers
   - Click "Predict" button
   - Verify prediction result displays
   - Verify no errors in browser console

4. ✅ **Error handling**
   - Test with invalid input
   - Test with empty input
   - Verify appropriate error messages

### Automated E2E Testing (Optional)

For automated E2E testing, consider using:
- **Playwright** or **Cypress** for browser automation
- **Pytest with Selenium** for Python-based E2E tests

Example Playwright setup (optional):
```bash
cd frontend
npm install -D @playwright/test
npx playwright install
```

---

## Running All Tests

### Quick Test Commands

**Backend only:**
```bash
cd backend
poetry run pytest
```

**Frontend only:**
```bash
cd frontend
npm test -- --run
```

**Both (in sequence):**
```bash
# Backend
cd backend && poetry run pytest && cd ..

# Frontend
cd frontend && npm test -- --run && cd ..
```

### Pre-commit Testing

Consider adding a test script to run before commits:

```bash
#!/bin/bash
# test-all.sh

echo "Running backend tests..."
cd backend && poetry run pytest && cd ..

echo "Running frontend tests..."
cd frontend && npm test -- --run && cd ..

echo "All tests passed!"
```

Make it executable:
```bash
chmod +x test-all.sh
./test-all.sh
```

---

## Test Coverage

### Backend Coverage

```bash
cd backend
pytest --cov=app --cov-report=html --cov-report=term
```

View detailed coverage:
- Terminal: Coverage summary printed
- HTML: Open `htmlcov/index.html` in browser

### Frontend Coverage

```bash
cd frontend
npm run test:coverage
```

Coverage report will be displayed in terminal and saved to `coverage/` directory.

### Coverage Goals

- **Backend**: Aim for >80% coverage on API endpoints
- **Frontend**: Aim for >70% coverage on components
- **Critical paths**: 100% coverage (health checks, main prediction flow)

---

## Troubleshooting

### Backend Tests Failing

1. **Check dependencies**:
   ```bash
   cd backend
   poetry install
   ```

2. **Verify Python version**:
   ```bash
   python --version  # Should be 3.12+
   ```

3. **Check model loading**:
   - Ensure models are available
   - Check model paths in configuration

### Frontend Tests Failing

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Clear cache**:
   ```bash
   rm -rf node_modules/.vite
   ```

3. **Check TypeScript errors**:
   ```bash
   npm run build
   ```

### Integration Issues

1. **Check CORS settings** if frontend can't reach backend
2. **Verify ports** are not in use
3. **Check Docker logs**:
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```

---

## Best Practices

1. **Write tests first** (TDD) when possible
2. **Keep tests isolated** - each test should be independent
3. **Use descriptive test names** - `test_predict_endpoint_with_valid_input`
4. **Mock external dependencies** - don't rely on external services
5. **Test edge cases** - empty inputs, invalid data, errors
6. **Keep tests fast** - unit tests should run in milliseconds
7. **Maintain test coverage** - aim for high coverage on critical paths

---

## Next Steps

- [ ] Add more comprehensive test cases
- [ ] Set up CI/CD pipeline with automated testing
- [ ] Add performance/load testing
- [ ] Set up automated E2E testing
- [ ] Add contract testing between frontend and backend

---

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

