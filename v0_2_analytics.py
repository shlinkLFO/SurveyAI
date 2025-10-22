from __future__ import annotations

from typing import Dict, List

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.decomposition import PCA


QUESTION_COLUMNS: List[str] = [f"q{i}" for i in range(1, 7)]
QUESTION_LABELS: List[str] = [f"Q{i}" for i in range(1, 7)]


def _compute_cronbach_alpha(df: pd.DataFrame) -> float:
    """Compute Cronbach's alpha for the question columns.

    Alpha = (k/(k-1)) * (1 - sum(var_i)/var_total)
    where var_total is the variance of the total score across items.
    """
    items = df[QUESTION_COLUMNS].to_numpy(dtype=float)
    if items.shape[0] < 2:
        return float("nan")

    k = items.shape[1]
    item_variances = items.var(axis=0, ddof=1)
    total_scores = items.sum(axis=1)
    total_variance = total_scores.var(ddof=1)

    if total_variance <= 0:
        return float("nan")

    alpha = (k / (k - 1.0)) * (1.0 - (item_variances.sum() / total_variance))
    return float(alpha)


def _compute_pca(df: pd.DataFrame) -> Dict[str, List[float]]:
    """Run PCA on question columns and return explained variance ratios."""
    X = df[QUESTION_COLUMNS].to_numpy(dtype=float)
    # Centering is done by PCA by default (with whiten=False)
    pca = PCA()
    pca.fit(X)
    variance_ratios = pca.explained_variance_ratio_.tolist()
    components = list(range(1, len(variance_ratios) + 1))
    return {
        "components": components,
        "variance": variance_ratios,
    }


def _compute_correlation(df: pd.DataFrame) -> List[List[float]]:
    corr = df[QUESTION_COLUMNS].corr(method="pearson")
    return corr.values.tolist()


def _compute_covariance(df: pd.DataFrame) -> List[List[float]]:
    cov = df[QUESTION_COLUMNS].cov()
    return cov.values.tolist()


def _compute_kmo_from_corr(corr: np.ndarray) -> float:
    """Compute overall KMO from a correlation matrix.

    KMO = sum(r_ij^2) / (sum(r_ij^2) + sum(p_ij^2)) for i<j,
    where p_ij are partial correlations derived from the precision matrix.
    """
    k = corr.shape[0]
    if k < 2:
        return float("nan")

    # Ensure symmetry and numerical stability
    C = np.array(corr, dtype=float)
    C = (C + C.T) / 2.0
    # Add small ridge if needed for invertibility
    eps = 1e-8
    try:
        P = np.linalg.inv(C)
    except np.linalg.LinAlgError:
        P = np.linalg.inv(C + eps * np.eye(k))

    # Partial correlation between i and j from precision matrix
    partial = np.zeros_like(C)
    for i in range(k):
        for j in range(k):
            if i == j:
                partial[i, j] = 1.0
            else:
                denom = np.sqrt(P[i, i] * P[j, j])
                if denom <= 0:
                    partial[i, j] = 0.0
                else:
                    partial[i, j] = -P[i, j] / denom

    # Sum of squared correlations and partial correlations, off-diagonal only
    r2_sum = 0.0
    p2_sum = 0.0
    for i in range(k):
        for j in range(i + 1, k):
            r2_sum += (C[i, j] ** 2)
            p2_sum += (partial[i, j] ** 2)

    denom = r2_sum + p2_sum
    if denom <= 0:
        return float("nan")
    return float(r2_sum / denom)


def _regression_summary_text(df: pd.DataFrame) -> str:
    """Return a compact OLS summary for one representative model.

    We model q6 as a function of the other 5 questions to keep text concise.
    """
    try:
        predictors = [q for q in QUESTION_COLUMNS if q != "q6"]
        X = sm.add_constant(df[predictors].to_numpy(dtype=float))
        y = df["q6"].to_numpy(dtype=float)
        model = sm.OLS(y, X, hasconst=True).fit()
        # Keep the standard text summary; consumer will render in <pre>
        return model.summary().as_text()
    except Exception as exc:
        return f"Regression unavailable: {exc}"


def generate_analytics_payload(responses: List[Dict]) -> Dict:
    """Generate analytics JSON payload from raw response dicts.

    Structure matches expectations of the v0.2 upgrades UI (Plotly page):
      - corr_matrix: 2D list of Pearson r values (Q1-Q6 only)
      - corr_matrix_with_age: 2D list including age dummies
      - columns: list of question labels [Sentience, EQ2030, ...]
      - columns_with_age: includes age dummy labels
      - pca_components: [1..k]
      - pca_variance: explained variance ratios per component
      - cronbach_alpha: float
      - regression_summary: text block for one OLS model
    """
    df = pd.DataFrame(responses)
    if df.empty or any(col not in df.columns for col in QUESTION_COLUMNS):
        return {
            "corr_matrix": [],
            "columns": ["Sentience", "EQ2030", "Reliance", "Future Education", "Understanding", "Social Impact"],
            "corr_matrix_with_age": [],
            "columns_with_age": [],
            "pca_components": [],
            "pca_variance": [],
            "cronbach_alpha": float("nan"),
            "kmo": float("nan"),
            "regression_summary": "No data available.",
        }

    # Descriptive labels
    descriptive_labels = ["Sentience", "EQ2030", "Reliance", "Future Education", "Understanding", "Social Impact"]
    
    # One-hot encode age if available - drop first to avoid multicollinearity
    age_dummy_cols = []
    age_dummy_labels = []
    if 'age_group' in df.columns:
        age_dummies = pd.get_dummies(df['age_group'], prefix='age', drop_first=True)
        df = pd.concat([df, age_dummies], axis=1)
        age_dummy_cols = list(age_dummies.columns)
        # Reference category is '16-18', so we label the remaining 4
        age_label_map = {
            'age_19-22': 'Undergrad',
            'age_23-26': 'Graduate',
            'age_27-40': 'Working',
            'age_40+': 'Older'
        }
        age_dummy_labels = [age_label_map.get(col, col) for col in age_dummy_cols]
    
    feature_cols = QUESTION_COLUMNS + age_dummy_cols
    df_q = df[feature_cols].dropna()
    if len(df_q) < 2:
        return {
            "corr_matrix": [[0.0] * 6 for _ in range(6)],
            "columns": descriptive_labels,
            "corr_matrix_with_age": [],
            "columns_with_age": [],
            "pca_components": [],
            "pca_variance": [],
            "cronbach_alpha": float("nan"),
            "kmo": float("nan"),
            "regression_summary": "Need at least 2 complete responses.",
        }

    # Correlation/Covariance: Q1-Q6 only
    corr_df = df_q[QUESTION_COLUMNS].corr(method="pearson")
    corr_matrix = corr_df.values.tolist()
    cov_matrix = df_q[QUESTION_COLUMNS].cov().values.tolist()
    
    # Correlation/Covariance: Q1-Q6 + Age dummies
    if age_dummy_cols:
        corr_df_with_age = df_q[QUESTION_COLUMNS + age_dummy_cols].corr(method="pearson")
        corr_matrix_with_age = corr_df_with_age.values.tolist()
        cov_matrix_with_age = df_q[QUESTION_COLUMNS + age_dummy_cols].cov().values.tolist()
        columns_with_age = descriptive_labels + age_dummy_labels
    else:
        corr_matrix_with_age = corr_matrix
        cov_matrix_with_age = cov_matrix
        columns_with_age = descriptive_labels
    
    # PCA on questions only
    pca_info = _compute_pca(df_q[QUESTION_COLUMNS])
    alpha = _compute_cronbach_alpha(df_q[QUESTION_COLUMNS])
    try:
        kmo_val = _compute_kmo_from_corr(np.array(df_q[QUESTION_COLUMNS].corr(method="pearson").values.tolist()))
    except Exception:
        kmo_val = float("nan")
    reg_summary = _regression_summary_text(df_q[QUESTION_COLUMNS])

    def _s(val):
        if isinstance(val, float):
            if np.isnan(val) or np.isinf(val):
                return None
            return float(val)
        if isinstance(val, list):
            return [_s(v) for v in val]
        if isinstance(val, dict):
            return {k: _s(v) for k, v in val.items()}
        return val

    payload = {
        "corr_matrix": corr_matrix,
        "columns": descriptive_labels,
        "corr_matrix_with_age": _s(corr_matrix_with_age),
        "cov_matrix_with_age": _s(cov_matrix_with_age),
        "columns_with_age": columns_with_age,
        "pca_components": pca_info["components"],
        "pca_variance": _s(pca_info["variance"]),
        "cronbach_alpha": _s(alpha),
        "kmo": _s(kmo_val),
        "regression_summary": reg_summary,
        "cov_matrix": _s(cov_matrix),
        "n": int(len(df_q)),
    }
    return payload


