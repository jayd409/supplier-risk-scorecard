import numpy as np
import pandas as pd

np.random.seed(42)

def generate_suppliers(n=150):
    """Generate 150 realistic global suppliers with real country/industry patterns."""

    # Real supplier company naming patterns by country
    supplier_names = {
        'China': ['Shenzhen Tech Mfg', 'Shanghai Electronics', 'Guangzhou Parts', 'Chengdu Components',
                  'Beijing Industrial', 'Ningbo Manufacturing', 'Suzhou Precision', 'Foshan Metal'],
        'India': ['Tata Suppliers', 'Mumbai Industrial', 'Bangalore Parts', 'Chennai Manufacturing',
                  'Gurgaon Components', 'Hyderabad Electronics', 'Pune Precision', 'Delhi Industrial'],
        'Vietnam': ['Hanoi Industrial', 'HCMC Textiles', 'Hai Phong Manufacturing', 'Da Nang Components',
                    'Vinh Textile Mills', 'Thai Nguyen Steel', 'Quang Ninh Industrial', 'Ben Tre Manufacturing'],
        'Germany': ['Siemens Supplier', 'Munich Precision', 'Stuttgart Engineering', 'Hamburg Metals',
                    'Berlin Industrial', 'Cologne Chemicals', 'Frankfurt Components', 'Nuremberg Parts'],
        'Japan': ['Tokyo Manufacturing', 'Osaka Precision', 'Yokohama Industrial', 'Kobe Steel Works',
                  'Nagoya Components', 'Kyoto Electronics', 'Fukuoka Parts', 'Sapporo Manufacturing'],
        'USA': ['Detroit Automotive', 'Texas Chemicals', 'California Tech', 'New York Industrial',
                'Ohio Manufacturing', 'Florida Components', 'Pennsylvania Steel', 'Illinois Parts'],
        'Mexico': ['Mexico City Industrial', 'Monterrey Manufacturing', 'Guadalajara Parts', 'Puebla Components',
                   'Tijuana Electronics', 'Juarez Manufacturing', 'Leon Automotive', 'Merida Components'],
        'Brazil': ['São Paulo Industrial', 'Rio de Janeiro Parts', 'Belo Horizonte Manufacturing', 'Salvador Components',
                   'Recife Textiles', 'Brasilia Industrial', 'Manaus Manufacturing', 'Curitiba Metals'],
        'Taiwan': ['Taipei Manufacturing', 'Taichung Electronics', 'Kaohsiung Industrial', 'Tainan Components',
                   'Hsinchu Precision', 'Keelung Shipping', 'Chiayi Manufacturing', 'Yunlin Industrial'],
        'South Korea': ['Seoul Electronics', 'Busan Industrial', 'Incheon Manufacturing', 'Daegu Components',
                        'Daejeon Tech', 'Gwangju Manufacturing', 'Ulsan Chemicals', 'Sejong Industrial'],
        'Belgium': ['Antwerp Chemicals', 'Brussels Industrial', 'Ghent Manufacturing', 'Liege Steel'],
        'Netherlands': ['Amsterdam Industrial', 'Rotterdam Chemicals', 'The Hague Components', 'Utrecht Manufacturing'],
    }

    # Industry categories with typical country patterns
    categories = {
        'Electronics': ['China', 'Taiwan', 'South Korea', 'Vietnam', 'USA', 'Japan'],
        'Textiles': ['Vietnam', 'India', 'China', 'Mexico', 'Brazil'],
        'Automotive': ['Germany', 'Japan', 'USA', 'Mexico', 'South Korea'],
        'Raw Materials': ['Brazil', 'India', 'China', 'USA', 'Mexico'],
        'Chemicals': ['Germany', 'USA', 'Belgium', 'China', 'India'],
    }

    suppliers = []
    rng = np.random.default_rng(42)

    for i in range(n):
        supplier_id = f'SUP{i+1:03d}'

        # Select category and appropriate country
        category = np.random.choice(list(categories.keys()))
        country = np.random.choice(categories[category])

        # Get a realistic company name
        if country in supplier_names:
            name = f"{np.random.choice(supplier_names[country])} #{i+1}"
        else:
            name = f"{country} Supplier {i+1}"

        # Tier distribution: 40% tier-1, 40% tier-2, 20% tier-3
        tier = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])

        # Annual spend: realistic distribution ($50K - $5M)
        # Tier-1 typically higher spend
        if tier == 1:
            annual_spend = np.random.uniform(500000, 5000000)
        elif tier == 2:
            annual_spend = np.random.uniform(200000, 1500000)
        else:
            annual_spend = np.random.uniform(50000, 500000)

        # On-time delivery: realistic by country (China: 82%, Japan/Germany: 95%, India: 80%)
        if country in ['Japan', 'Germany', 'South Korea']:
            on_time_delivery = np.random.uniform(0.92, 0.98)
        elif country in ['USA', 'Taiwan']:
            on_time_delivery = np.random.uniform(0.85, 0.95)
        elif country == 'Brazil':
            on_time_delivery = np.random.uniform(0.75, 0.88)
        else:  # China, Vietnam, India, etc.
            on_time_delivery = np.random.uniform(0.75, 0.90)

        # Quality defect rate: realistic by country
        if country in ['Japan', 'Germany']:
            defect_rate = np.random.uniform(0.001, 0.03)
        elif country in ['USA', 'South Korea', 'Taiwan']:
            defect_rate = np.random.uniform(0.01, 0.05)
        else:  # China, India, Vietnam
            defect_rate = np.random.uniform(0.02, 0.08)

        # Lead time: varies by geography and production
        if country == 'USA':
            lead_time = np.random.uniform(5, 15)
        elif country in ['Mexico', 'Canada']:
            lead_time = np.random.uniform(8, 20)
        elif country in ['Germany', 'Japan', 'South Korea']:
            lead_time = np.random.uniform(15, 35)
        else:  # Asia, Brazil
            lead_time = np.random.uniform(20, 60)

        # Financial stability score (1-10): generally higher for developed countries
        if country in ['Germany', 'USA', 'Japan']:
            financial_stability = int(np.random.uniform(7, 10))
        elif country in ['South Korea', 'Taiwan']:
            financial_stability = int(np.random.uniform(6, 9))
        elif country in ['Brazil', 'Mexico']:
            financial_stability = int(np.random.uniform(4, 8))
        else:  # China, India, Vietnam
            financial_stability = int(np.random.uniform(3, 7))

        # Dependency percentage (how much they depend on us)
        dependency_pct = np.random.uniform(2, 60)

        # Years active with us
        years_active = np.random.randint(1, 21)

        # Number of incidents (quality/delivery/compliance issues)
        if on_time_delivery > 0.90 and defect_rate < 0.03:
            incidents = np.random.randint(0, 3)  # Low-risk suppliers
        elif on_time_delivery > 0.75 and defect_rate < 0.06:
            incidents = np.random.randint(1, 6)  # Medium-risk
        else:
            incidents = np.random.randint(3, 10)  # Higher-risk

        suppliers.append({
            'supplier_id': supplier_id,
            'name': name,
            'country': country,
            'category': category,
            'tier': tier,
            'annual_spend': round(annual_spend, 2),
            'on_time_delivery_rate': round(on_time_delivery, 3),
            'quality_defect_rate': round(defect_rate, 4),
            'lead_time_days': int(lead_time),
            'financial_stability_score': financial_stability,
            'dependency_pct': round(dependency_pct, 2),
            'years_active': years_active,
            'num_incidents': incidents
        })

    return pd.DataFrame(suppliers)
