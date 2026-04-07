# Supplier Risk Scorecard

Scores 150 suppliers across 12 countries. Japan/Germany 95% on-time delivery; India/Vietnam 80-85%. Consolidates supplier risk into single scorecard enabling procurement optimization and diversification decisions.

## Business Question
Which suppliers pose operational risk and where should we diversify sourcing?

## Key Findings
- 150 suppliers across 12 countries analyzed on delivery, defect, responsiveness metrics
- On-time delivery variance: Japan 95%, Germany 95%, China 87%, India 82%, Vietnam 80%
- Defect rate variance: Japan 0.5%, Germany 0.8%, India 2.1%, Vietnam 2.8%—quality tier effect
- Risk concentration: top 5 suppliers = 45% spend; diversification with India/Vietnam suppliers adds 18% spend

## How to Run
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
python3 main.py
```
Open `outputs/supplier_dashboard.html` in your browser.

## Project Structure
- **src/supplier_data.py** - Supplier performance dataset
- **src/scorer.py** - Risk scoring algorithm
- **src/supplier_analysis.py** - Cohort and concentration analysis
- **src/supplier_charts.py** - Risk heatmap, tier distribution

## Tech Stack
Python, Pandas, NumPy, Matplotlib, Seaborn, SQLite

## Author
Jay Desai · [jayd409@gmail.com](mailto:jayd409@gmail.com) · [Portfolio](https://jayd409.github.io)
