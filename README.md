# AI Confidence Survey - UIUC MS Business Analytics

FastAPI-powered survey application with advanced statistical analysis.

## Live Application

- Survey: https://glowstone.red/SurveyAI-UIUC

## Features

- Interactive Survey: 6 AI-related confidence questions (-1 to +1 scale)
- Real-time Visualizations: Histograms with mean indicators and outlier detection
- Multivariate Regression: OLS/Ridge regression with statsmodels
- Advanced Analytics: Correlation matrices, covariance, PCA, Cronbach's Alpha, KMO
- Admin Dashboard: Data management, export, deletion, synthetic data generation

## Technical Stack

**Backend:** FastAPI, Statsmodels, Scikit-learn, Pandas, NumPy, Uvicorn
**Frontend:** React 18, Chart.js, Tailwind CSS
**Deployment:** cPanel/Passenger, Systemd, JSON storage

## Project Structure

```
SurveyAI/
├── main.py                 # FastAPI backend
├── v0_2_analytics.py       # Advanced analytics
├── index.html             # Survey interface
├── requirements.txt        # Dependencies
└── docs/                  # Deployment guides
```

## Quick Start

```bash
pip install -r requirements.txt
python main.py
# Access at http://localhost:8000
```

**Deployment:** See [docs/QUICK_START_CPANEL.md](docs/QUICK_START_CPANEL.md) or [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## API Endpoints

- `GET /` - Survey page
- `GET /api/responses` - Get all responses
- `POST /api/submit` - Submit response
- `GET /api/regression` - Regression analysis
- `GET /api/regression-age` - Age-based models
- `GET /api/analytics` - Advanced analytics
- `POST /api/admin/export` - Export data (admin)
- `POST /api/admin/clear` - Clear data (admin)
- `POST /api/admin/generate` - Generate samples (admin)
- `POST /api/admin/delete` - Delete response (admin)

API docs: `/docs`

## Security

- SHA-256 password authentication. Default: `PA$$`
- Update in `main.py` line 37: `ADMIN_PASSWORD_HASH = hashlib.sha256(b"your_password").hexdigest()`

## Survey Questions

1. Humans have access to sentient AI today
2. AI outperforms humans on EQ exam by 2030
3. I can compete in job market without AI
4. Child born today faces harder path to higher education (HS 2044)
5. I understand how Multi-Modal ML/AI models decide
6. AI positively impacts my social circle by 2035

## Analytics Features

**Distributions:** 9 equal-width histograms, mean line, outlier highlighting (Pink: |Z| >= 2.24, Red: |Z| >= 2.89)

**Regression:** 6 models (question vs others + age), Beta/SE/t-stats/P-values, R²/Adj R²/RMSE, age prediction

**Advanced:** Correlation/Covariance matrices, PCA, Cronbach's Alpha, KMO, rolling trends, scatter plots

## Data Format

```json
{
  "responses": [{
    "timestamp": "2025-10-22T12:00:00Z",
    "age_group": "23-26",
    "q1": 0.5, "q2": -0.3, "q3": 0.1,
    "q4": 0.2, "q5": -0.4, "q6": 0.6
  }]
}
```

## License & Authors

~Mason 'A' "ShlinkLFO" Beydoun
GLOWSTONE LLC
PORTAL@GLOWSTONE.LLC
MIT License - UIUC MS Business Analytics Program
