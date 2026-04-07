import pandas as pd
import numpy as np

def risk_by_country(df):
    """Average risk score by country."""
    return df.groupby('country')['risk_score'].agg(['mean', 'count']).sort_values('mean', ascending=False).head(10)

def risk_by_category(df):
    """Average risk score by category."""
    return df.groupby('category')['risk_score'].agg(['mean', 'count']).sort_values('mean', ascending=False)

def risk_by_tier(df):
    """Average risk score by supplier tier."""
    return df.groupby('tier')['risk_score'].agg(['mean', 'count']).sort_values('mean', ascending=False)

def top_risk_suppliers(df, n=20):
    """Top N highest risk suppliers."""
    return df.nlargest(n, 'risk_score')[['supplier_id', 'name', 'country', 'category', 'risk_score', 'risk_tier']]

def spend_concentration(df):
    """Top suppliers by annual spend and their % of total."""
    total_spend = df['annual_spend'].sum()
    top_spend = df.nlargest(10, 'annual_spend').copy()
    top_spend['pct_of_total'] = (top_spend['annual_spend'] / total_spend * 100).round(2)
    return top_spend[['supplier_id', 'name', 'annual_spend', 'pct_of_total', 'risk_tier']]

def risk_stats(df):
    """Summary statistics on risk distribution."""
    return {
        'low': (df['risk_tier'] == 'Low').sum(),
        'medium': (df['risk_tier'] == 'Medium').sum(),
        'high': (df['risk_tier'] == 'High').sum(),
        'total': len(df)
    }
