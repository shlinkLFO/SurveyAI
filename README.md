# AI Confidence Survey - UIUC MS Business Analytics

FastAPI-powered survey application with advanced statistical analysis using Python's scientific computing stack.

## 🚀 Live Application

- **Survey**: https://glowstone.red/SurveyAIUIUC
- **Admin Panel**: https://glowstone.red/SurveyAIUIUC/admin (password protected)
- **GitHub**: https://github.com/shlinkLFO/SurveyAI

## ✨ Features

- **Interactive Survey**: 6 AI-related confidence questions with slider inputs (-1 to +1 scale)
- **Real-time Visualizations**: Histograms with mean indicators using Chart.js
- **Multivariate Regression**: Python-powered OLS/Ridge regression with statsmodels
- **Advanced Analytics**: Correlation matrices, covariance analysis, PCA
- **Admin Dashboard**: Data management, export, and synthetic data generation
- **RESTful API**: Clean FastAPI backend with automatic documentation

## 📊 Technical Stack

**Backend:**
- FastAPI (Python 3.9+)
- Statsmodels & Scikit-learn for regression
- Pandas & NumPy for data processing
- Uvicorn ASGI server

**Frontend:**
- React 18 (via CDN)
- Chart.js for visualizations
- Tailwind CSS for styling
- Babel Standalone for JSX

**Deployment:**
- cPanel/Passenger support (NameCheap Stellar)
- Systemd service for VPS
- JSON file storage

## 🎯 Key Upgrade: JavaScript → Python

**Why we switched from Node.js to FastAPI:**

✅ **Better Statistics**: Native support for advanced regression analysis  
✅ **Handles Multicollinearity**: Automatic fallback to Ridge regression  
✅ **Numerical Stability**: Python's scientific libraries are industry-standard  
✅ **P-values & T-stats**: Proper statistical inference with statsmodels  
✅ **Faster Development**: Rich ecosystem for data science  

## 📁 Project Structure

```
SurveyAI/
├── main.py                 # FastAPI backend with regression endpoints
├── passenger_wsgi.py       # cPanel/Passenger entry point
├── index.html             # Main survey interface
├── 84Metashosan.html      # Admin panel
├── requirements.txt        # Python dependencies
├── .htaccess              # Apache/Passenger configuration
├── survey-data.json       # Data storage (not in repo)
├── docs/                  # Deployment guides
│   ├── CPANEL_DEPLOYMENT.md
│   ├── DEPLOYMENT.md
│   ├── QUICK_START_CPANEL.md
│   └── START_HERE.txt
├── install.sh             # Local installation script
├── start.sh               # Development server launcher
└── surveyai.service       # Systemd service file
```

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
# or
uvicorn main:app --reload

# Access at http://localhost:8000
```

### cPanel Deployment (NameCheap Stellar)

See **[docs/QUICK_START_CPANEL.md](docs/QUICK_START_CPANEL.md)** for 5-minute deployment guide.

### VPS/SSH Deployment

See **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** for full deployment instructions.

## 📡 API Endpoints

- `GET /` - Main survey page
- `GET /admin` - Admin panel
- `GET /api/responses` - Get all survey responses
- `POST /api/submit` - Submit new response
- `GET /api/regression` - Get regression analysis
- `POST /api/admin/export` - Export data (admin only)
- `POST /api/admin/clear` - Clear all data (admin only)
- `POST /api/admin/generate` - Generate sample data (admin only)

Full API docs available at `/docs` when running the server.

## 🔒 Security

- Admin endpoints protected by password authentication
- SHA-256 password hashing
- Hidden admin panel (not linked from main page)
- CORS enabled for cross-origin requests
- Data stored server-side only

**Default admin password**: `password` (CHANGE THIS!)

To update password, edit `main.py` line 22:
```python
import hashlib
ADMIN_PASSWORD_HASH = hashlib.sha256(b"your_new_password").hexdigest()
```

## 📊 Survey Questions

1. As of today, humans have access to sentient AI
2. AI will outperform humans on a standardized exam for Emotional Intelligence: EQ by 2030
3. I could compete in the job market without leveraging AI
4. A child born Fall 2025 will complete HS in Spring of 2044...
5. I understand how Machine Learning AI models make decisions
6. AI will have a net positive impact on your closest social circle/s in a decade

## 🔬 Research Application

**UIUC MS Business Analytics Research Project**

This application is designed to collect confidence scores on AI-related statements and perform multivariate statistical analysis to understand relationships between different dimensions of AI confidence.

## 📈 Analytics Features

**Distributions Page:**
- Histograms with 0.25 bin size
- Red vertical line showing mean
- Mean and standard deviation displayed

**Regression Page:**
- 6 multivariate regression models
- Each question predicted by the other 5
- Beta coefficients, standard errors, t-statistics
- P-values and significance indicators
- Adjusted R², R², RMSE

**Advanced Analytics:**
- Pearson correlation matrix
- Covariance matrix (color-coded)
- Variance analysis by question
- PCA visualization
- Confidence trend over time

## 🛠️ Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests (if implemented)
pytest
```

## 📝 Data Format

Survey responses are stored in JSON format:
```json
{
  "responses": [
    {
      "timestamp": "2025-10-21T12:00:00Z",
      "q1": 0.5,
      "q2": -0.3,
      "q3": 0.1,
      "q4": 0.2,
      "q5": -0.4,
      "q6": 0.6
    }
  ]
}
```

## 🤝 Contributing

This is a research project. For questions or issues:
1. Open an issue on GitHub
2. Contact the research team

## 📄 License

MIT License - See LICENSE file for details

## 👥 Authors

UIUC MS Business Analytics Program

## 🔗 Links

- **Live Application**: https://glowstone.red/SurveyAIUIUC
- **GitHub Repository**: https://github.com/shlinkLFO/SurveyAI
- **UIUC Gies College of Business**: https://giesbusiness.illinois.edu/

---

**Previous Version**: This project was previously built with Node.js/Express. See git history for the JavaScript version. The current Python/FastAPI version provides superior statistical analysis capabilities.
