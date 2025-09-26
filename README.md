# TravelMate - Vacation Planner Mobile App

A comprehensive vacation planning mobile application built with Python, featuring cross-platform support for iOS and Android using Kivy/KivyMD for the frontend and FastAPI for the backend.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure email/password registration and login
- **Trip Management**: Create, view, edit, and delete vacation trips
- **Itinerary Planning**: Day-by-day activity planning with drag-and-drop reordering
- **Budget Tracking**: Expense logging with category breakdown and analytics
- **Packing Lists**: Categorized packing items with check-off functionality
- **Real-time Collaboration**: WebSocket-based real-time sync for shared trips
- **Offline Support**: Local data caching for offline functionality

### Advanced Features
- **Weather Integration**: Weather forecasts for trip destinations
- **Maps Integration**: Static map previews for activity locations
- **Currency Converter**: Built-in currency conversion for international trips
- **Smart Suggestions**: Pre-defined lists for common packing items
- **Visual Analytics**: Pie charts and progress tracking

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with async/await support
- **Database**: MongoDB with Motor async driver
- **Authentication**: JWT-based authentication with bcrypt password hashing
- **Real-time**: WebSocket support for collaborative features
- **API**: RESTful API with comprehensive CRUD operations

### Frontend (KivyMD)
- **Framework**: Kivy with KivyMD Material Design components
- **State Management**: Internal Kivy properties and data models
- **HTTP Client**: httpx for asynchronous API calls
- **Local Storage**: JsonStore for offline data persistence
- **WebSockets**: Real-time communication with backend

## 📁 Project Structure

```
vacation-planner/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # MongoDB connection
│   ├── models.py               # Pydantic data models
│   ├── auth.py                 # Authentication utilities
│   ├── routers/                # API route handlers
│   │   ├── auth_router.py      # Authentication endpoints
│   │   ├── trips_router.py     # Trip management endpoints
│   │   ├── activities_router.py # Activity management endpoints
│   │   ├── expenses_router.py  # Expense management endpoints
│   │   └── packing_router.py   # Packing list endpoints
│   └── requirements.txt        # Backend dependencies
├── frontend/
│   ├── main.py                 # KivyMD application entry point
│   ├── screens/                # UI screens
│   │   ├── auth_screen.py      # Login/register screen
│   │   ├── dashboard_screen.py # Trip dashboard
│   │   ├── trip_detail_screen.py # Trip detail view
│   │   ├── create_trip_screen.py # Trip creation form
│   │   ├── overview_tab.py     # Trip overview tab
│   │   ├── itinerary_tab.py    # Itinerary planning tab
│   │   ├── budget_tab.py       # Budget tracking tab
│   │   └── packing_tab.py      # Packing list tab
│   ├── utils/                  # Utility modules
│   │   ├── api_client.py       # API communication
│   │   └── websocket_client.py # WebSocket communication
│   └── requirements.txt        # Frontend dependencies
└── README.md                   # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MongoDB Atlas account (or local MongoDB instance)
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vacation-planner
   ```

2. **Navigate to backend directory**
   ```bash
   cd backend
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment**
   - Update `config.py` with your MongoDB connection string
   - Change the secret key for production use

6. **Run the backend server**
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Update API URL**
   - Edit `utils/api_client.py` and change `self.base_url` to your backend URL

5. **Run the mobile app**
   ```bash
   python main.py
   ```

## 📱 Usage

### Getting Started
1. **Register**: Create a new account with email and password
2. **Login**: Sign in to access your trips
3. **Create Trip**: Tap the + button to create your first vacation
4. **Plan**: Add activities, track expenses, and manage packing lists
5. **Collaborate**: Share trips with travel companions for real-time collaboration

### Key Features

#### Trip Dashboard
- View all your trips (upcoming, ongoing, past)
- Quick access to trip creation
- Trip status and countdown timers

#### Itinerary Planning
- Add activities with time, location, and cost
- Organize by day with drag-and-drop reordering
- Activity types: food, transport, activity, lodging

#### Budget Tracking
- Set overall trip budget
- Log expenses by category
- Real-time budget vs. spent tracking
- Visual analytics and category breakdown

#### Packing Lists
- Categorized items (clothes, toiletries, electronics, documents)
- Check-off functionality
- Progress tracking
- Smart suggestions for common items

## 🔧 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Trips
- `GET /trips/` - Get user trips
- `POST /trips/` - Create new trip
- `GET /trips/{trip_id}` - Get trip details
- `PUT /trips/{trip_id}` - Update trip
- `DELETE /trips/{trip_id}` - Delete trip

### Activities
- `GET /activities/{trip_id}` - Get trip activities
- `POST /activities/{trip_id}` - Create activity
- `PUT /activities/{trip_id}/{activity_id}` - Update activity
- `DELETE /activities/{trip_id}/{activity_id}` - Delete activity

### Expenses
- `GET /expenses/{trip_id}` - Get trip expenses
- `POST /expenses/{trip_id}` - Create expense
- `GET /expenses/{trip_id}/summary` - Get expense summary

### Packing
- `GET /packing/{trip_id}` - Get packing items
- `POST /packing/{trip_id}` - Create packing item
- `PUT /packing/{trip_id}/{item_id}/toggle` - Toggle item packed status

### WebSocket
- `WS /ws/{trip_id}` - Real-time collaboration for trip

## 🚀 Deployment

### Backend Deployment
1. **Heroku**: Use the included `Procfile` and deploy to Heroku
2. **Docker**: Build and deploy using Docker containers
3. **Cloud Run**: Deploy to Google Cloud Run for serverless scaling

### Frontend Deployment
1. **Buildozer**: Use Buildozer to create APK/IPA files
2. **KivyMD**: Package for mobile app stores
3. **Desktop**: Run directly on desktop platforms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation
- Review the API endpoints

## 🔮 Future Enhancements

- [ ] Social authentication (Google, Apple)
- [ ] Advanced weather integration
- [ ] Interactive maps with route planning
- [ ] Photo sharing and trip memories
- [ ] Export functionality (PDF, calendar)
- [ ] Advanced analytics and insights
- [ ] Multi-language support
- [ ] Dark mode theme
- [ ] Push notifications
- [ ] Offline map support

---

**TravelMate** - Making vacation planning simple, collaborative, and enjoyable! 🌍✈️




