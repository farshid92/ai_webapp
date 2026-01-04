# 🚀 Quick Start - Run on Localhost

## Method 1: Manual (Recommended for First Time)

### Step 1: Start Backend

Open **Terminal 1**:
```bash
cd backend
poetry install        # First time only
poetry shell
uvicorn app.main:app --reload
```

✅ Backend running at: **http://localhost:8000**

### Step 2: Start Frontend

Open **Terminal 2**:
```bash
cd frontend
npm install          # First time only
npm run dev
```

✅ Frontend running at: **http://localhost:5173**

### Step 3: Open Browser

Navigate to: **http://localhost:5173**

---

## Method 2: Using Script (If Terminal Emulator Available)

```bash
./start-dev.sh
```

This will open both services in separate terminal windows.

---

## Method 3: Docker Compose

```bash
docker-compose up --build
```

✅ Frontend: **http://localhost:3000**  
✅ Backend: **http://localhost:8000**

---

## 🧪 Test It Works

1. **Open**: http://localhost:5173
2. **Enter**: `1, 2, 3, 4` in the input field
3. **Click**: "Predict" button
4. **Verify**: Prediction result appears

---

## 📚 API Documentation

Visit: **http://localhost:8000/docs**

Interactive API documentation where you can test all endpoints.

---

## 🔧 Troubleshooting

**Backend won't start?**
```bash
cd backend
poetry install
poetry shell
uvicorn app.main:app --reload
```

**Frontend won't start?**
```bash
cd frontend
npm install
npm run dev
```

**Port already in use?**
- Backend: Change port with `--port 8001`
- Frontend: Vite will auto-use next available port

**CORS errors?**
- Make sure backend is running
- Check browser console (F12) for details

---

## 📖 Full Documentation

See [RUN_LOCALLY.md](./RUN_LOCALLY.md) for detailed instructions.


