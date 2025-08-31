import pandas as pd
import numpy as np

def generate_sample_data(n=100):
    np.random.seed(42)  # For reproducibility
    data = {
        'transaction_id': range(1, n+1),
        'account_id': np.random.randint(1, 10, n),
        'from_account': np.random.choice(['A', 'B', 'C', 'External'], n),
        'to_account': np.random.choice(['A', 'B', 'C', 'Internal'], n),
        'amount': np.random.uniform(100, 15000, n),
        'timestamp': pd.date_range(start='2025-01-01', periods=n, freq='h'),
        'kyc_verified': np.random.choice([True, False], n, p=[0.8, 0.2])
    }
    df = pd.DataFrame(data)
    
    # Simulate smurfing: 15 small transactions for account 1
    smurf_data = {
        'transaction_id': range(n+1, n+16),
        'account_id': 1,
        'from_account': 'External',
        'to_account': 'A',
        'amount': np.full(15, 500),
        'timestamp': pd.date_range(start='2025-01-05', periods=15, freq='min'),
        'kyc_verified': True
    }
    smurf_df = pd.DataFrame(smurf_data)
    
    # Simulate layering: 6 rapid transfers for account 2
    layer_data = {
        'transaction_id': range(n+16, n+22),
        'account_id': 2,
        'from_account': ['A', 'B', 'C', 'A', 'B', 'C'],
        'to_account': ['B', 'C', 'A', 'B', 'C', 'External'],
        'amount': np.full(6, 2000),
        'timestamp': pd.date_range(start='2025-01-10', periods=6, freq='10min'),
        'kyc_verified': False
    }
    layer_df = pd.DataFrame(layer_data)
    
    df = pd.concat([df, smurf_df, layer_df], ignore_index=True)
    df.to_csv('data/transactions.csv', index=False)
    print(f"Generated {len(df)} sample transactions in data/transactions.csv")

if __name__ == "__main__":
    generate_sample_data()