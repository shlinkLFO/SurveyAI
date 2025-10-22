from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import os
from datetime import datetime
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import hashlib
from v0_2_analytics import generate_analytics_payload

app = FastAPI(
    title="AI Confidence Survey - UIUC",
    root_path="/SurveyAI-UIUC"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
# Use absolute path to ensure data file is found regardless of working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "survey-data.json")
REMINDERS_FILE = os.path.join(BASE_DIR, "reminder-data.json")
ADMIN_PASSWORD_HASH = "3dd7f1eb8e998529db00ed23f9a37845297a27a79b1cfc8c0d5cef2d8468b3ee"  # "PA$$"

# Models
class SurveyResponse(BaseModel):
    timestamp: str
    age_group: str
    q1: float
    q2: float
    q3: float
    q4: float
    q5: float
    q6: float

class AdminAuth(BaseModel):
    password: str

class GenerateSamplesRequest(BaseModel):
    password: str
    num_responses: int
    distribution_type: str

class ReminderRequest(BaseModel):
    email: str
    response_count: int
    timestamp: str

# Helper functions
def load_data():
    """Load survey data from JSON file"""
    if not os.path.exists(DATA_FILE):
        return {"responses": []}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    """Save survey data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_reminders():
    """Load reminder data from JSON file"""
    if not os.path.exists(REMINDERS_FILE):
        return {"reminders": []}
    with open(REMINDERS_FILE, 'r') as f:
        return json.load(f)

def save_reminders(data):
    """Save reminder data to JSON file"""
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def verify_admin_password(password: str) -> bool:
    """Verify admin password"""
    return hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH

def calculate_regression_models(df: pd.DataFrame):
    """Calculate multivariate regression for each question with age bins as predictors"""
    questions = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']
    results = []
    
    q_label_map = {
        0: "Sentience",
        1: "EQ2030", 
        2: "Reliance",
        3: "Future Education",
        4: "Understanding",
        5: "Social Impact"
    }
    
    # One-hot encode age if available - drop first to avoid multicollinearity
    age_dummy_cols = []
    age_dummy_labels = []
    if 'age_group' in df.columns:
        dummies = pd.get_dummies(df['age_group'], prefix='age', drop_first=True)
        # Convert boolean dummies to float to avoid numpy type errors
        for col in dummies.columns:
            dummies[col] = dummies[col].astype(float)
        df = pd.concat([df, dummies], axis=1)
        age_dummy_cols = list(dummies.columns)
        # First category '16-18' is dropped, so remaining 4:
        age_label_map = {
            'age_19-22': 'Age 19-22',
            'age_23-26': 'Age 23-26',
            'age_27-40': 'Age 27-40',
            'age_40+': 'Age 40+'
        }
        age_dummy_labels = [age_label_map.get(col, col) for col in age_dummy_cols]

    for target_idx, target_col in enumerate(questions):
        try:
            # Prepare data: other Q features + age dummies
            predictor_cols = [q for q in questions if q != target_col] + age_dummy_cols

            # Drop rows with any missing values in predictors or target
            model_cols = [target_col] + predictor_cols
            df_model = df[model_cols].dropna()

            # Require sufficient observations (need more than # of predictors + constant)
            min_required = len(predictor_cols) + 2
            if len(df_model) < min_required:
                print(f"Skipping {target_col}: insufficient complete rows ({len(df_model)}/{len(df)}) for {len(predictor_cols)} predictors (need >= {min_required})")
                continue

            X = df_model[predictor_cols].values
            y = df_model[target_col].values
            
            # Add constant for intercept
            X_with_const = sm.add_constant(X)
            
            # Fit OLS model
            print(f"Fitting {target_col}: n={len(df_model)}, p={len(predictor_cols)}")
            model = sm.OLS(y, X_with_const).fit()
            print(f"Successfully fit {target_col}: R²={model.rsquared:.4f}")
            
            # Build predictor labels
            predictor_indices = [i for i in range(6) if i != target_idx]
            predictor_short_labels = [q_label_map[i] for i in predictor_indices]
            all_predictor_labels = predictor_short_labels + age_dummy_labels

            results.append({
                'targetQuestion': f'Question {target_idx + 1}',
                'targetIdx': target_idx,
                'predictorIndices': predictor_indices,
                'predictorLabels': all_predictor_labels,
                'beta': model.params.tolist(),
                'standardErrors': model.bse.tolist(),
                'tStats': model.tvalues.tolist(),
                'pValues': model.pvalues.tolist(),
                'r2': float(model.rsquared),
                'adjR2': float(model.rsquared_adj),
                'rmse': float(np.sqrt(model.mse_resid)),
                'n': int(model.nobs),
                'method': 'OLS'
            })
            
        except Exception as e:
            print(f"Error calculating regression for {target_col}: {e}")
            continue
    
    return results

# API Endpoints

@app.get("/")
async def read_root():
    """Serve the main survey page"""
    return FileResponse("index.html")

@app.get("/admin")
async def read_admin():
    """Serve the admin page"""
    return FileResponse("84Metashosan.html")

@app.get("/upgrades")
async def read_upgrades():
    """Serve the v0.2 upgrades demo page (Advanced Analytics)."""
    return FileResponse("gpt-atlas-upgrades.html")

@app.get("/api/responses")
async def get_responses():
    """Get all survey responses"""
    data = load_data()
    return JSONResponse(content=data.get("responses", []))

@app.post("/api/submit")
async def submit_response(response: SurveyResponse):
    """Submit a new survey response"""
    data = load_data()
    
    # Add new response
    data.setdefault("responses", []).append(response.dict())
    
    # Save updated data
    save_data(data)
    
    return JSONResponse(content={
        "success": True,
        "count": len(data["responses"])
    })

@app.post("/api/reminder")
async def submit_reminder(reminder: ReminderRequest):
    """Submit email reminder request"""
    reminder_data = load_reminders()
    
    # Add new reminder
    reminder_data.setdefault("reminders", []).append(reminder.dict())
    
    # Save updated reminders
    save_reminders(reminder_data)
    
    return JSONResponse(content={
        "success": True,
        "count": len(reminder_data["reminders"])
    })

@app.get("/api/regression")
async def get_regression():
    """Calculate and return regression analysis"""
    data = load_data()
    responses = data.get("responses", [])
    
    if len(responses) < 6:
        raise HTTPException(
            status_code=400,
            detail="Need at least 6 responses for regression analysis"
        )
    
    # Convert to DataFrame
    df = pd.DataFrame(responses)
    
    # Calculate regression models
    results = calculate_regression_models(df)

    # Remove separate age model block; age effects appear via one-hot dummies in each model
    
    # If nothing could be computed, return an empty list (200) so UI can handle gracefully
    if not results:
        return JSONResponse(content=[])
    
    # Sanitize NaN/Inf for JSON
    def _safe(val):
        try:
            if isinstance(val, float):
                if np.isnan(val) or np.isinf(val):
                    return None
                return float(val)
            if isinstance(val, (int, str)):
                return val
            if isinstance(val, list):
                return [_safe(v) for v in val]
            if isinstance(val, dict):
                return {k: _safe(v) for k, v in val.items()}
            return val
        except Exception:
            return None

    safe_results = [_safe(r) for r in results]
    return JSONResponse(content=safe_results)

@app.get("/api/regression-age")
async def get_regression_age():
    """Regression predicting each age bin (binary classification) from the six questions."""
    data = load_data()
    responses = data.get("responses", [])
    if len(responses) < 6:
        raise HTTPException(status_code=400, detail="Need at least 6 responses for regression analysis")

    df = pd.DataFrame(responses)
    if 'age_group' not in df.columns:
        raise HTTPException(status_code=400, detail="No age data available")

    df = df.dropna(subset=['age_group'])
    
    age_bins = ['16-18', '19-22', '23-26', '27-40', '40+']
    age_labels = ['Teen', 'Undergrad', 'Graduate', 'Working', 'Older']
    predictor_labels = ["Sentience", "EQ2030", "Reliance", "Future Education", "Understanding", "Social Impact"]
    
    results = []
    
    for age_bin, age_label in zip(age_bins, age_labels):
        # Create binary target: 1 if this age bin, 0 otherwise
        df[f'is_{age_bin}'] = (df['age_group'] == age_bin).astype(float)
        
        # Count how many samples in this bin
        count = df[f'is_{age_bin}'].sum()
        
        if count < 2:
            continue  # Skip if insufficient samples
        
        X = df[['q1','q2','q3','q4','q5','q6']].values
        y = df[f'is_{age_bin}'].values
        X_with_const = sm.add_constant(X)
        
        try:
            model = sm.OLS(y, X_with_const).fit()
            result = {
                'targetQuestion': f'Age: {age_label} ({age_bin})',
                'targetIdx': -1,
                'ageBin': age_bin,
                'ageLabel': age_label,
                'count': int(count),
                'predictorLabels': predictor_labels,
                'beta': model.params.tolist(),
                'standardErrors': model.bse.tolist(),
                'tStats': model.tvalues.tolist(),
                'pValues': model.pvalues.tolist(),
                'r2': float(model.rsquared),
                'adjR2': float(model.rsquared_adj),
                'rmse': float(np.sqrt(model.mse_resid)),
                'n': int(model.nobs),
                'method': 'OLS'
            }
            results.append(result)
        except Exception as e:
            print(f"Error computing regression for {age_bin}: {e}")
            continue
    
    # Sort by count (most responses first)
    results.sort(key=lambda x: x['count'], reverse=True)

    # sanitize
    def _safe(val):
        try:
            if isinstance(val, float):
                if np.isnan(val) or np.isinf(val):
                    return None
                return float(val)
            if isinstance(val, (int, str)):
                return val
            if isinstance(val, list):
                return [_safe(v) for v in val]
            if isinstance(val, dict):
                return {k: _safe(v) for k, v in val.items()}
            return val
        except Exception:
            return None
    
    return JSONResponse(content=[_safe(r) for r in results])

@app.get("/api/analytics")
async def get_analytics():
    """Return advanced analytics JSON for the v0.2 upgrades UI."""
    data = load_data()
    responses = data.get("responses", [])
    payload = generate_analytics_payload(responses)
    return JSONResponse(content=payload)

@app.post("/api/admin/export")
async def admin_export(auth: AdminAuth):
    """Export all data (admin only)"""
    if not verify_admin_password(auth.password):
        raise HTTPException(status_code=403, detail="Invalid password")
    
    data = load_data()
    return JSONResponse(content=data.get("responses", []))

@app.post("/api/admin/clear")
async def admin_clear(auth: AdminAuth):
    """Clear all data (admin only)"""
    if not verify_admin_password(auth.password):
        raise HTTPException(status_code=403, detail="Invalid password")
    
    save_data({"responses": []})
    return JSONResponse(content={"success": True})

@app.post("/api/admin/generate")
async def generate_samples(request: GenerateSamplesRequest):
    """Generate random sample responses (admin only)"""
    if not verify_admin_password(request.password):
        raise HTTPException(status_code=403, detail="Invalid password")
    
    data = load_data()
    responses = data.setdefault("responses", [])
    
    # Generate samples
    for _ in range(request.num_responses):
        timestamp = datetime.now().isoformat()
        
        if request.distribution_type == "normal":
            values = np.random.normal(0, 0.3, 6)
        elif request.distribution_type == "uniform":
            values = np.random.uniform(-1, 1, 6)
        elif request.distribution_type == "bimodal":
            values = []
            for _ in range(6):
                peak = 0.5 if np.random.random() > 0.5 else -0.5
                values.append(np.clip(np.random.normal(peak, 0.2), -1, 1))
            values = np.array(values)
        else:
            values = np.random.uniform(-1, 1, 6)
        
        # Clip to [-1, 1] range
        values = np.clip(values, -1, 1)
        
        response = {
            "timestamp": timestamp,
            "age_group": np.random.choice(["16-18","19-22","23-26","27-40","40+"], p=[0.1,0.4,0.3,0.15,0.05]).item(),
            "q1": float(round(values[0], 2)),
            "q2": float(round(values[1], 2)),
            "q3": float(round(values[2], 2)),
            "q4": float(round(values[3], 2)),
            "q5": float(round(values[4], 2)),
            "q6": float(round(values[5], 2)),
        }
        responses.append(response)
    
    save_data(data)
    
    return JSONResponse(content={
        "success": True,
        "generated": request.num_responses,
        "total": len(responses)
    })

@app.post("/api/admin/reminders")
async def admin_get_reminders(auth: AdminAuth):
    """Get all reminder requests (admin only)"""
    if not verify_admin_password(auth.password):
        raise HTTPException(status_code=403, detail="Invalid password")
    
    reminder_data = load_reminders()
    return JSONResponse(content=reminder_data.get("reminders", []))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

