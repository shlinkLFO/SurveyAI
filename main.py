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

app = FastAPI(
    title="AI Confidence Survey - UIUC"
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
DATA_FILE = "survey-data.json"
ADMIN_PASSWORD_HASH = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"  # "password"

# Models
class SurveyResponse(BaseModel):
    timestamp: str
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

def verify_admin_password(password: str) -> bool:
    """Verify admin password"""
    return hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH

def calculate_regression_models(df: pd.DataFrame):
    """Calculate multivariate regression for each question"""
    questions = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']
    results = []
    
    for target_idx, target_col in enumerate(questions):
        try:
            # Prepare data
            predictor_cols = [q for q in questions if q != target_col]
            X = df[predictor_cols].values
            y = df[target_col].values
            
            # Add constant for intercept
            X_with_const = sm.add_constant(X)
            
            # Fit OLS model with Ridge regularization for stability
            try:
                # Try standard OLS first
                model = sm.OLS(y, X_with_const).fit()
            except:
                # Fall back to Ridge if singular matrix
                ridge = Ridge(alpha=0.001)
                ridge.fit(X, y)
                
                # Calculate stats manually for Ridge
                y_pred = ridge.predict(X)
                n = len(y)
                p = len(predictor_cols)
                
                # R-squared
                ss_res = np.sum((y - y_pred) ** 2)
                ss_tot = np.sum((y - np.mean(y)) ** 2)
                r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                adj_r2 = 1 - ((1 - r2) * (n - 1) / (n - p - 1))
                
                # RMSE
                rmse = np.sqrt(mean_squared_error(y, y_pred))
                
                results.append({
                    'targetQuestion': f'Question {target_idx + 1}',
                    'targetIdx': target_idx,
                    'predictorIndices': [i for i in range(6) if i != target_idx],
                    'beta': [ridge.intercept_] + ridge.coef_.tolist(),
                    'standardErrors': [0.0] * (len(predictor_cols) + 1),  # Not available for Ridge
                    'tStats': [0.0] * (len(predictor_cols) + 1),
                    'pValues': [1.0] * (len(predictor_cols) + 1),
                    'r2': float(r2),
                    'adjR2': float(adj_r2),
                    'rmse': float(rmse),
                    'n': int(n),
                    'method': 'Ridge'
                })
                continue
            
            # Extract statistics from OLS model
            predictor_indices = [i for i in range(6) if i != target_idx]
            
            results.append({
                'targetQuestion': f'Question {target_idx + 1}',
                'targetIdx': target_idx,
                'predictorIndices': predictor_indices,
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
    
    if not results:
        raise HTTPException(
            status_code=500,
            detail="Unable to calculate regression models"
        )
    
    return JSONResponse(content=results)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

