import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from analysis import top_risk_suppliers, risk_by_country

def risk_tier_distribution(df):
    """Chart 1: Risk tier distribution (pie)."""
    tier_counts = df['risk_tier'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}
    color_list = [colors.get(t, 'gray') for t in tier_counts.index]
    ax.pie(tier_counts.values, labels=tier_counts.index, autopct='%1.1f%%', colors=color_list)
    ax.set_title('Risk Tier Distribution', fontsize=12, fontweight='bold')
    return fig

def top_risk_suppliers_chart(df):
    """Chart 2: Top 20 riskiest suppliers (horizontal bar, colored by tier)."""
    top_20 = top_risk_suppliers(df, 20)
    colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}
    color_list = [colors.get(t, 'gray') for t in top_20['risk_tier']]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(range(len(top_20)), top_20['risk_score'], color=color_list)
    ax.set_yticks(range(len(top_20)))
    ax.set_yticklabels(top_20['supplier_id'], fontsize=8)
    ax.set_title('Top 20 Riskiest Suppliers', fontsize=12, fontweight='bold')
    ax.set_xlabel('Risk Score')
    return fig

def risk_by_category_box(df):
    """Chart 3: Risk score by category (box plot)."""
    fig, ax = plt.subplots(figsize=(10, 5))
    categories = df['category'].unique()
    box_data = [df[df['category'] == cat]['risk_score'].values for cat in categories]
    bp = ax.boxplot(box_data, labels=categories, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
    ax.set_title('Risk Score Distribution by Category', fontsize=12, fontweight='bold')
    ax.set_ylabel('Risk Score')
    ax.tick_params(axis='x', rotation=45)
    return fig

def spend_vs_risk_bubble(df):
    """Chart 4: Spend vs risk scatter (bubble: size=spend)."""
    fig, ax = plt.subplots(figsize=(10, 5))
    scatter = ax.scatter(df['risk_score'], df['annual_spend'],
                        s=df['annual_spend']/5000, alpha=0.6, c=df['risk_score'],
                        cmap='RdYlGn_r')
    ax.set_title('Spend vs Risk Score', fontsize=12, fontweight='bold')
    ax.set_xlabel('Risk Score')
    ax.set_ylabel('Annual Spend ($)')
    plt.colorbar(scatter, ax=ax)
    return fig

def delivery_vs_defect(df):
    """Chart 5: On-time delivery vs defect rate (colored by risk)."""
    colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red'}
    color_list = [colors.get(t, 'gray') for t in df['risk_tier']]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(df['on_time_delivery_rate'], df['quality_defect_rate'],
              c=color_list, s=100, alpha=0.6)
    ax.set_title('On-Time Delivery vs Defect Rate', fontsize=12, fontweight='bold')
    ax.set_xlabel('On-Time Delivery Rate')
    ax.set_ylabel('Quality Defect Rate')

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=l) for l, c in colors.items()]
    ax.legend(handles=legend_elements, loc='best')
    return fig

def country_risk_heatmap(df):
    """Chart 6: Country risk heatmap (top 10)."""
    country_risk = risk_by_country(df).head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(country_risk.index, country_risk['mean'], color='steelblue')

    # Color bars by risk
    for i, (idx, val) in enumerate(country_risk['mean'].items()):
        if val > 66:
            bars[i].set_color('red')
        elif val > 33:
            bars[i].set_color('orange')
        else:
            bars[i].set_color('green')

    ax.set_title('Average Risk Score by Country (Top 10)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Avg Risk Score')
    return fig
