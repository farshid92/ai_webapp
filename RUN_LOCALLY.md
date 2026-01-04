# Running the Application Locally

This guide shows you how to run both the backend and frontend on your localhost for development and testing.

## 🚀 Quick Start

### Option 1: Run Both Services Separately (Recommended for Development)

**Terminal 1 - Backend:**
```bash
cd backend
poetry install  # First time only
poetry shell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install  # First time only
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### Option 2: Using Docker Compose (Production-like)

```bash
docker-compose up --build
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📋 Detailed Instructions

### Prerequisites

1. **Backend:**
   - Python 3.12+
   - Poetry installed (`pip install poetry`)

2. **Frontend:**
   - Node.js 18+ and npm

3. **Docker (Optional):**
   - Docker and Docker Compose installed

---

## 🔧 Backend Setup

### First Time Setup

```bash
cd backend
poetry install
```

### Running the Backend

```bash
# Activate virtual environment
poetry shell

# Run with auto-reload (development)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or run without reload
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Backend will be available at:**
- API: `http://localhost:8000`
- Interactive API Docs: `http://localhost:8000/docs`
- Alternative API Docs: `http://localhost:8000/redoc`

### Test Backend

```bash
# Health check
curl http://localhost:8000/health

# List models
curl http://localhost:8000/api/models/

# Make a prediction
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"inputs": [1.0, 2.0, 3.0, 4.0], "model_name": "base"}'
```

---

## 🎨 Frontend Setup

### First Time Setup

```bash
cd frontend
npm install
```

### Running the Frontend

```bash
npm run dev
```

**Frontend will be available at:**
- Development server: `http://localhost:5173` (Vite default port)
- The frontend is configured to proxy `/api` requests to `http://localhost:8000`

### Frontend Development

The Vite dev server includes:
- Hot Module Replacement (HMR) - changes reflect instantly
- Proxy configuration - `/api` requests go to backend
- Fast refresh - React components update without losing state

---

## 🔗 How They Connect

### Development Mode

1. **Frontend** runs on `http://localhost:5173` (Vite dev server)
2. **Backend** runs on `http://localhost:8000` (FastAPI/Uvicorn)
3. **Vite Proxy** automatically forwards `/api/*` requests to `http://localhost:8000`
4. **CORS** is configured in the backend to allow requests from `http://localhost:5173`

### Request Flow

```
Browser → http://localhost:5173/api/predict
         ↓ (Vite proxy)
         → http://localhost:8000/api/predict
         ↓ (FastAPI backend)
         → Response
```

---

## 🐳 Docker Compose Setup

### Build and Run

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Access Services

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

---

## 🧪 Testing the Integration

### 1. Start Both Services

**Terminal 1:**
```bash
cd backend
poetry shell
uvicorn app.main:app --reload
```

**Terminal 2:**
```bash
cd frontend
npm run dev
```

### 2. Open Browser

Navigate to: `http://localhost:5173`

### 3. Test the Application

1. Enter comma-separated numbers: `1, 2, 3, 4`
2. Click "Predict" button
3. Verify the prediction result appears
4. Check browser console (F12) for any errors

### 4. Test API Directly

Open API docs: `http://localhost:8000/docs`

Try the `/api/predict/` endpoint:
- Click "Try it out"
- Enter: `{"inputs": [1.0, 2.0, 3.0, 4.0], "model_name": "base"}`
- Click "Execute"
- Verify response

---

## 🔍 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
uvicorn app.main:app --reload --port 8001
```

**Dependencies not installed:**
```bash
cd backend
poetry install
```

**Model not found:**
- Check if model files exist in `backend/ml/checkpoints/`
- For testing, models are mocked in tests

### Frontend Issues

**Port already in use:**
```bash
# Vite will automatically use next available port
# Or specify port:
npm run dev -- --port 5174
```

**Dependencies not installed:**
```bash
cd frontend
npm install
```

**CORS errors:**
- Ensure backend is running
- Check CORS configuration in `backend/app/main.py`
- Verify frontend is accessing `http://localhost:5173` (not `http://127.0.0.1:5173`)

**API requests failing:**
- Verify backend is running on port 8000
- Check browser console for errors
- Verify Vite proxy configuration in `frontend/vite.config.ts`

### Docker Issues

**Build fails:**
```bash
# Rebuild without cache
docker-compose build --no-cache
```

**Services won't start:**
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose restart
```

---

## 📝 Environment Variables (Optional)

### Backend

Create `backend/.env`:
```env
PORT=8000
DEBUG=true
```

### Frontend

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

---

## 🎯 Quick Reference

| Service | Command | URL |
|---------|---------|-----|
| Backend | `uvicorn app.main:app --reload` | http://localhost:8000 |
| Frontend | `npm run dev` | http://localhost:5173 |
| API Docs | Auto-available | http://localhost:8000/docs |
| Docker | `docker-compose up` | http://localhost:3000 (frontend) |

---

## ✅ Checklist

Before testing:
- [ ] Backend dependencies installed (`poetry install`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Browser console shows no errors
- [ ] API docs accessible at `/docs`

---

## 🚀 Next Steps

1. **Make changes** - Both services support hot reload
2. **Test changes** - Refresh browser to see updates
3. **Check logs** - Monitor terminal output for errors
4. **Use API docs** - Test endpoints interactively at `/docs`

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [Testing Guide](./TESTING_GUIDE.md)


