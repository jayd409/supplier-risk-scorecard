import sys
sys.path.insert(0, 'src')

from supplier_data import generate_suppliers
from database import save_to_db, query
from scorer import score_suppliers
from supplier_analysis import top_risk_suppliers, spend_concentration, risk_stats
from supplier_charts import (risk_tier_distribution, top_risk_suppliers_chart, risk_by_category_box,
                    spend_vs_risk_bubble, delivery_vs_defect, country_risk_heatmap)
from utils import save_html

df = generate_suppliers(150)
df = score_suppliers(df)

save_to_db(df, 'suppliers')

top_risk = top_risk_suppliers(df, 1)
top_risk_name = top_risk.iloc[0]['name'] if len(top_risk) > 0 else 'N/A'
stats = risk_stats(df)
total_spend = df['annual_spend'].sum()

charts = [
    ('Risk Tier Distribution', risk_tier_distribution(df)),
    ('Top 20 Riskiest Suppliers', top_risk_suppliers_chart(df)),
    ('Risk by Category', risk_by_category_box(df)),
    ('Spend vs Risk', spend_vs_risk_bubble(df)),
    ('Delivery vs Defect', delivery_vs_defect(df)),
    ('Country Risk Heatmap', country_risk_heatmap(df))
]

kpis = [
    ('Total Suppliers', str(len(df))),
    ('High Risk', str(stats['high'])),
    ('Total Spend', f"${total_spend/1e6:.1f}M"),
]

save_html(charts, 'Supplier Risk Scorecard', kpis, 'outputs/supplier_dashboard.html')

print(f"Suppliers: 150 | High Risk: {stats['high']} | Total Spend: ${total_spend/1e6:.1f}M | Top risk: {top_risk_name}")

# --- SQL Analytics (SQLite) ---
print("\n--- SQL Analytics (SQLite) ---")

# Query 1: Supplier count and avg risk score by risk tier
print("\n1. Supplier Count and Avg Risk Score by Risk Tier:")
sql_tier = """
SELECT risk_tier, COUNT(*) as supplier_count,
       ROUND(AVG(risk_score), 2) as avg_risk_score,
       ROUND(MIN(risk_score), 2) as min_score,
       ROUND(MAX(risk_score), 2) as max_score,
       ROUND(SUM(annual_spend) / 1000000.0, 1) as total_spend_millions
FROM suppliers
GROUP BY risk_tier
ORDER BY CASE WHEN risk_tier = 'High' THEN 1 WHEN risk_tier = 'Medium' THEN 2 ELSE 3 END
"""
result_tier = query(sql_tier)
print(result_tier.to_string(index=False))

# Query 2: Total spend and avg risk by category
print("\n2. Total Spend and Avg Risk by Category:")
sql_category = """
SELECT category, COUNT(*) as supplier_count,
       ROUND(SUM(annual_spend) / 1000000.0, 1) as total_spend_millions,
       ROUND(AVG(risk_score), 2) as avg_risk_score,
       ROUND(AVG(on_time_delivery_rate), 3) as avg_delivery_rate,
       ROUND(AVG(quality_defect_rate), 4) as avg_defect_rate
FROM suppliers
GROUP BY category
ORDER BY total_spend_millions DESC
"""
result_category = query(sql_category)
print(result_category.to_string(index=False))

# Query 3: Top 10 highest risk suppliers
print("\n3. Top 10 Highest Risk Suppliers:")
sql_top_risk = """
SELECT supplier_id, name, category, country, risk_score, risk_tier,
       ROUND(annual_spend / 1000000.0, 2) as spend_millions,
       ROUND(on_time_delivery_rate, 3) as delivery_rate,
       quality_defect_rate, num_incidents
FROM suppliers
ORDER BY risk_score DESC
LIMIT 10
"""
result_top_risk = query(sql_top_risk)
print(result_top_risk.to_string(index=False))
