# Website Monitoring and Security Platform

A comprehensive SaaS platform for monitoring websites, tracking performance, validating SSL certificates, and analyzing security posture. This platform provides real-time monitoring, alerts, and a detailed dashboard for tracking multiple websites.

## 🌟 Features

- **Website Monitoring**
  - Uptime tracking
  - Response time monitoring
  - Performance metrics
  - Status code tracking

- **Security Analysis**
  - SSL certificate validation
  - Security headers analysis
  - Security posture scoring
  - Real-time security alerts

- **Dashboard**
  - Interactive metrics visualization
  - Real-time status updates
  - Historical data tracking
  - Custom monitoring intervals

## 🛠️ Tech Stack

- **Backend**
  - FastAPI (API framework)
  - SQLAlchemy (ORM)
  - Alembic (Database migrations)
  - PostgreSQL (Database)
  - Python 3.9+

- **Frontend**
  - Streamlit (Dashboard)
  - Plotly (Data visualization)
  - Pandas (Data processing)

## 📋 Prerequisites

1. Python 3.9 or higher
2. PostgreSQL 12 or higher
3. Git

## 🚀 Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/website-monitoring-platform.git
cd website-monitoring-platform
```

### 2. Set Up PostgreSQL
```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE monitoring_db;

-- Create user (optional)
CREATE USER monitoring_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE monitoring_db TO monitoring_user;

-- Exit PostgreSQL
\q
```

### 3. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/monitoring_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Monitoring Configuration
MONITORING_INTERVAL_SECONDS=300
SSL_CHECK_INTERVAL_HOURS=24

# Alert Configuration (Optional)
ALERT_EMAIL_ENABLED=false
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
```

### 5. Initialize Database
```bash
# Navigate to backend directory
cd backend

# Create and apply migrations
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

### 6. Start the Application

#### Start Backend Server
```bash
# From backend directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Start Frontend Server
```bash
# Open new terminal and activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/MacOS

# Start Streamlit
cd frontend
streamlit run app.py
```

## 📁 Project Structure
```
project/
├── backend/
│   ├── main.py           # FastAPI application entry point
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Database connection
│   ├── services/
│   │   ├── monitor_service.py    # Monitoring logic
│   │   └── security_service.py   # Security analysis
│   ├── routes/
│   │   ├── monitor.py    # Monitoring endpoints
│   │   └── website.py    # Website management
│   └── alembic/          # Database migrations
├── frontend/
│   ├── app.py           # Streamlit dashboard
│   └── components/      # UI components
├── tests/               # Test files
├── requirements.txt     # Project dependencies
└── .env                # Environment variables
```

## 🖥️ Dashboard Access & Getting Started

1. Create a user account:
   - Go to http://localhost:8000/docs (FastAPI Swagger UI)
   - Scroll to the POST /users/ endpoint
   - Click "Try it out"
   - Enter your email and password in JSON format:
     ```json
     {
       "email": "your.email@example.com",
       "password": "your_password"
     }
     ```
   - Click "Execute" to create your account

2. Access the dashboard:
   - Go to http://localhost:8501
   - Log in with your credentials
   - Start monitoring websites using the sidebar form

3. Once logged in, you can:
   - Add websites for monitoring
   - View website metrics and status
   - Check SSL certificates and security scores
   - Monitor response times and uptime
   - Use the refresh button to trigger immediate checks

## 🔧 Development Setup

1. **Install Development Dependencies**
```bash
pip install -r requirements-dev.txt
```

2. **Run Tests**
```bash
pytest
```

3. **Code Formatting**
```bash
# Format code
black .

# Sort imports
isort .

# Check types
mypy .
```

## 📝 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
```bash
git checkout -b feature/amazing-feature
```
3. Commit changes
```bash
git commit -m 'Add amazing feature'
```
4. Push to branch
```bash
git push origin feature/amazing-feature
```

## 🌱 Future Roadmap

- Multi-region monitoring
- AI-powered anomaly detection
- Advanced security scanning
- React-based frontend
- Mobile app support
- API rate limiting and quotas
