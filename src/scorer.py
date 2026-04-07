import numpy as np
import pandas as pd

WEIGHTS = {
    'delivery_risk':    0.25,  # 1 - on_time_delivery_rate
    'quality_risk':     0.20,  # defect_rate (normalized)
    'financial_risk':   0.20,  # 10 - financial_stability_score (normalized)
    'concentration':    0.15,  # dependency_pct
    'lead_time_risk':   0.10,  # lead_time_days (normalized)
    'incident_risk':    0.10,  # num_incidents (normalized)
}

def score_suppliers(df):
    """Calculate composite risk score for each supplier."""
    df = df.copy()

    def norm(s):
        """Normalize series to 0-1 range."""
        return (s - s.min()) / (s.max() - s.min() + 1e-8)

    # Calculate individual risk components
    df['delivery_risk']  = norm(1 - df['on_time_delivery_rate'])
    df['quality_risk']   = norm(df['quality_defect_rate'])
    df['financial_risk'] = norm(10 - df['financial_stability_score'])
    df['concentration']  = norm(df['dependency_pct'])
    df['lead_time_risk'] = norm(df['lead_time_days'])
    df['incident_risk']  = norm(df['num_incidents'])

    # Weighted sum
    df['risk_score'] = (
        df['delivery_risk'] * WEIGHTS['delivery_risk'] +
        df['quality_risk'] * WEIGHTS['quality_risk'] +
        df['financial_risk'] * WEIGHTS['financial_risk'] +
        df['concentration'] * WEIGHTS['concentration'] +
        df['lead_time_risk'] * WEIGHTS['lead_time_risk'] +
        df['incident_risk'] * WEIGHTS['incident_risk']
    )
    df['risk_score'] = (df['risk_score'] * 100).round(1)

    # Categorize risk
    df['risk_tier'] = pd.cut(df['risk_score'], bins=[0, 33, 66, 100], labels=['Low', 'Medium', 'High'])

    return df.sort_values('risk_score', ascending=False)
