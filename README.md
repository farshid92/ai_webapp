# AI Web Application - Machine Learning Prediction Service

A full-stack web application for deploying and serving machine learning models with a modern React frontend and FastAPI backend. This project demonstrates production-ready ML model deployment, RESTful API design, and comprehensive testing practices.

## 🎯 Project Overview

This application provides a complete ML model serving infrastructure with:
- **RESTful API** for model inference using FastAPI
- **Modern React Frontend** for interactive model predictions
- **PyTorch-based ML Models** with flexible architecture
- **Computer Vision**: U-Net for image segmentation
- **Ensemble Learning**: Multiple model combination strategies
- **Genetic Algorithms**: Hyperparameter optimization
- **Comprehensive Testing** (84% backend coverage, full frontend tests)
- **Docker Support** for containerized deployment
- **Production-ready** error handling and validation

## 🚀 Features

### Core Features
- **ML Model Serving**: Deploy and serve PyTorch models via REST API
- **Interactive UI**: React-based frontend for real-time predictions
- **Model Registry**: Manage multiple models with versioning support
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Comprehensive Testing**: Unit, integration, and E2E tests
- **Error Handling**: Robust error handling with clear user feedback
- **CORS Support**: Configured for cross-origin requests
- **Hot Reload**: Development-friendly with auto-reload

### Advanced ML Features ⭐
- **U-Net Segmentation**: Image segmentation using U-Net architecture
- **Ensemble Learning**: Combine multiple models (voting, averaging, weighted)
- **Genetic Algorithm**: Hyperparameter optimization using evolutionary algorithms
- **Image Processing**: Complete CV pipeline (preprocessing, post-processing, visualization)
- **Uncertainty Estimation**: Model prediction confidence metrics
- **Model Comparison**: Side-by-side performance evaluation

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PyTorch** - Deep learning framework
- **Torchvision** - Computer vision utilities
- **Pydantic** - Data validation
- **Poetry** - Dependency management
- **Pytest** - Testing framework
- **Uvicorn** - ASGI server
- **Pillow/OpenCV** - Image processing
- **DEAP** - Genetic algorithm library
- **Matplotlib** - Visualization

### Frontend
- **React 19** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Vitest** - Testing framework
- **React Testing Library** - Component testing

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Git** - Version control

## 📁 Project Structure

```
ai_webapp/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── ml/           # ML models and inference
│   │   ├── models/       # Pydantic schemas
│   │   └── main.py       # FastAPI application
│   ├── tests/            # Backend tests
│   └── pyproject.toml    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx       # Main React component
│   │   └── test/         # Frontend tests
│   └── package.json      # Node dependencies
├── docker-compose.yml    # Docker orchestration
├── TESTING_GUIDE.md      # Comprehensive testing docs
├── RUN_LOCALLY.md        # Local development guide
└── README.md             # This file
```

## 🏃 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- Poetry (`pip install poetry`)
- Docker (optional)

### Option 1: Local Development

**Backend:**
```bash
cd backend
poetry install
poetry shell
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Docker

```bash
docker-compose up --build
```

Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## 🧪 Testing

### Run All Tests

```bash
./test-all.sh
```

### Backend Tests

```bash
cd backend
poetry run pytest
poetry run pytest --cov=app  # With coverage
```

**Coverage: 84%** (10/10 tests passing)

### Frontend Tests

```bash
cd frontend
npm test -- --run
```

**Coverage: 7/7 tests passing**

See [TESTING_GUIDE.md](./TESTING_GUIDE.md) for detailed testing documentation.

## 📡 API Endpoints

### Core Endpoints
- `GET /health` - Health check
- `GET /api/models/` - List available models
- `GET /api/models/{model_name}` - Get model information
- `POST /api/predict/` - Regression prediction

### Computer Vision ⭐
- `POST /api/segmentation/predict` - Image segmentation (single image)
- `POST /api/segmentation/batch` - Batch image segmentation

### Ensemble Learning ⭐
- `POST /api/ensemble/predict` - Ensemble prediction
- `POST /api/ensemble/compare` - Compare multiple models
- `POST /api/ensemble/predict-with-uncertainty` - Prediction with confidence

### Optimization ⭐
- `POST /api/optimization/optimize` - Genetic algorithm hyperparameter optimization
- `GET /api/optimization/example-bounds` - Example parameter bounds

**Example - Image Segmentation**:
```bash
POST /api/segmentation/predict
Content-Type: multipart/form-data

file: <image_file>
model_name: "unet"
threshold: 0.5
overlay: true
```

**Example - Ensemble Prediction**:
```bash
POST /api/ensemble/predict
Content-Type: application/json

{
  "inputs": [1.0, 2.0, 3.0, 4.0],
  "model_names": ["base", "unet"]
}
```

Interactive API documentation available at `/docs` when backend is running.

## 🏗️ Architecture

### Backend Architecture

```
┌─────────────┐
│   FastAPI   │  ← REST API Layer
└──────┬──────┘
       │
┌──────▼──────┐
│ API Routes  │  ← Endpoint Handlers
└──────┬──────┘
       │
┌──────▼──────┐
│ ML Registry │  ← Model Management
└──────┬──────┘
       │
┌──────▼──────┐
│  Inference  │  ← Prediction Logic
└──────┬──────┘
       │
┌──────▼──────┐
│   PyTorch   │  ← Model Execution
└─────────────┘
```

### Frontend Architecture

```
┌─────────────┐
│   React     │  ← UI Components
└──────┬──────┘
       │
┌──────▼──────┐
│   Vite      │  ← Dev Server & Build
└──────┬──────┘
       │
┌──────▼──────┐
│   Proxy     │  ← API Requests
└──────┬──────┘
       │
┌──────▼──────┐
│  FastAPI    │  ← Backend API
└─────────────┘
```

## 🔧 Configuration

### Backend

- Python version: 3.12+
- Dependencies managed via Poetry
- Environment variables: None required (can be added for production)

### Frontend

- Node.js version: 18+
- Dependencies managed via npm
- Vite proxy configured for `/api` → `http://localhost:8000`

## 📊 Model Architectures

### RegressionNet (Default)
Feedforward neural network for regression tasks:

```
Input (4 features)
    ↓
Linear(4 → 64) + ReLU
    ↓
Linear(64 → 64) + ReLU
    ↓
Linear(64 → 1)
    ↓
Output (prediction)
```

### U-Net (Image Segmentation) ⭐
Encoder-decoder architecture with skip connections:

```
Input Image (3 channels, 256x256)
    ↓
Encoder Path (Downsampling)
    ├─ Conv → BN → ReLU → Conv → BN → ReLU
    ├─ MaxPool(2x2)
    ├─ [Repeat with increasing features: 64→128→256→512]
    ↓
Decoder Path (Upsampling)
    ├─ TransposeConv → Concatenate Skip Connection
    ├─ Conv → BN → ReLU → Conv → BN → ReLU
    ├─ [Repeat with decreasing features: 512→256→128→64]
    ↓
Output Mask (1 channel, 256x256)
```

**Key Features**:
- Skip connections preserve fine-grained details
- Symmetric encoder-decoder structure
- Variants: Standard, Small, Large

Models can be easily extended or replaced in `backend/app/ml/`.

## 🚢 Deployment

### Docker Deployment

```bash
docker-compose up -d
```

### Production Considerations

- Add environment variables for configuration
- Set up proper logging
- Configure reverse proxy (nginx)
- Add authentication/authorization
- Set up monitoring and alerting
- Use production-grade ASGI server (Gunicorn + Uvicorn workers)

## 📚 Documentation

- [Testing Guide](./TESTING_GUIDE.md) - Comprehensive testing documentation
- [Run Locally](./RUN_LOCALLY.md) - Detailed local development setup
- [Quick Start](./QUICK_START.md) - Quick reference guide
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (when running)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

See [LICENSE](./LICENSE) file for details.

## 🎓 Academic/Research Use

This project demonstrates:
- **Computer Vision**: U-Net segmentation, image processing pipelines
- **Advanced ML**: Ensemble learning, genetic algorithms, optimization
- **ML Model Deployment**: Production-ready model serving
- **Software Engineering**: Clean architecture, testing, documentation
- **Full-Stack Development**: Modern web technologies
- **DevOps Practices**: Docker, CI/CD ready

**Perfect for**:
- Computer Vision PhD applications
- ML Engineer positions
- Research project portfolios
- Full-stack ML development showcases

**Highlights**:
- ✅ U-Net implementation (classic CV architecture)
- ✅ Ensemble learning methods
- ✅ Genetic algorithm optimization
- ✅ Production deployment
- ✅ Comprehensive testing (84% coverage)

## 🔮 Future Enhancements

- [x] U-Net image segmentation
- [x] Ensemble learning
- [x] Genetic algorithm optimization
- [ ] Model training pipeline
- [ ] Model versioning system
- [ ] Frontend UI for image upload/visualization
- [ ] Performance metrics (IoU, Dice coefficient)
- [ ] Real dataset training
- [ ] Authentication and authorization
- [ ] Model performance monitoring
- [ ] CI/CD pipeline
- [ ] Kubernetes deployment
- [ ] Model explainability features

## 👤 Author

[Farshid Cheraghchian]

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- PyTorch for the ML framework
- React team for the UI library

---

⭐ If you find this project useful, please consider giving it a star!
