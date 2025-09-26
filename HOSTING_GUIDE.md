# 🚀 TravelMate Hosting Guide

## 📁 Project Structure for Hosting

```
vacation planner 1/
├── backend/                    # Backend API (FastAPI)
│   ├── run_backend.py         # Backend runner script
│   ├── main.py                # FastAPI app entry point
│   ├── requirements.txt       # Python dependencies
│   ├── Procfile              # Heroku deployment config
│   ├── runtime.txt           # Python version
│   └── env_template.txt      # Environment variables template
│
├── frontend/                   # Mobile App (KivyMD)
│   ├── run_frontend.py       # Frontend runner script
│   ├── main.py               # KivyMD app entry point
│   └── requirements.txt      # Python dependencies
│
└── run_app.py                # Development runner (root)
```

## 🏗️ Backend Hosting (API Server)

### Heroku Deployment

1. **Prepare Backend for Heroku:**
   ```bash
   cd backend
   cp env_template.txt .env
   # Edit .env with your actual values
   ```

2. **Deploy to Heroku:**
   ```bash
   # Initialize git repo in backend folder
   cd backend
   git init
   git add .
   git commit -m "Initial backend deployment"
   
   # Create Heroku app
   heroku create your-app-name-backend
   
   # Set environment variables
   heroku config:set MONGODB_URL="your-mongodb-url"
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set CORS_ORIGINS="https://yourdomain.com"
   
   # Deploy
   git push heroku main
   ```

3. **Backend will be available at:**
   ```
   https://your-app-name-backend.herokuapp.com
   ```

### Alternative Hosting (VPS/Cloud)

1. **Install Dependencies:**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   
   pip install -r requirements.txt
   ```

2. **Run Backend:**
   ```bash
   python run_backend.py
   ```

## 📱 Frontend Hosting (Mobile App)

### Build for Distribution

1. **Install Build Tools:**
   ```bash
   cd frontend
   pip install buildozer
   pip install cython
   ```

2. **Create buildozer.spec:**
   ```bash
   buildozer init
   # Edit buildozer.spec with your app details
   ```

3. **Build APK (Android):**
   ```bash
   buildozer android debug
   ```

4. **Build for iOS (requires macOS):**
   ```bash
   buildozer ios debug
   ```

### Development Testing

1. **Run Frontend:**
   ```bash
   cd frontend
   python run_frontend.py
   ```

## 🔧 Environment Configuration

### Required Environment Variables

Create a `.env` file in the backend folder with:

```env
# Database
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority&appName=your-app

# Security
SECRET_KEY=your-super-secret-key-change-in-production
CORS_ORIGINS=https://yourdomain.com,https://your-app.herokuapp.com

# Optional Features
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

## 🚀 Quick Start Commands

### Development
```bash
# Run both backend and frontend
python run_app.py

# Or run individually
cd backend && python run_backend.py
cd frontend && python run_frontend.py
```

### Production
```bash
# Backend only
cd backend && python run_backend.py

# Frontend build
cd frontend && buildozer android debug
```

## 📋 Pre-Deployment Checklist

- [ ] Update `SECRET_KEY` in production
- [ ] Configure `MONGODB_URL` for production database
- [ ] Set `CORS_ORIGINS` to include your frontend domain
- [ ] Configure Cloudinary for image uploads
- [ ] Test all API endpoints
- [ ] Build and test mobile app
- [ ] Set up monitoring and logging

## 🔗 API Endpoints

Once deployed, your backend will provide:

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user
- `GET /trips/` - Get user trips
- `POST /trips/` - Create new trip
- `POST /trips/join/{trip_id}` - Join trip
- `GET /trips/{trip_id}` - Get trip details
- `PUT /trips/{trip_id}` - Update trip
- `DELETE /trips/{trip_id}` - Delete trip

## 📞 Support

For hosting issues or questions, check:
1. Backend logs: `heroku logs --tail` (if using Heroku)
2. Frontend logs: Check console output
3. API testing: Use Postman or curl to test endpoints
