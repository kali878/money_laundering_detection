import pandas as pd
from .utils import load_data

def analyze_transactions(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(['account_id', 'timestamp'])
    
    # Compute velocity (rolling sum over 7 days)
    df['velocity'] = df.groupby('account_id')['amount'].rolling(window='7D').sum().reset_index(0, drop=True)
    
    # Time delta in minutes
    df['time_delta'] = df.groupby('account_id')['timestamp'].diff().dt.total_seconds() / 60
    df['time_delta'] = df['time_delta'].fillna(0)
    
    # Transaction count per account
    df['transaction_count'] = df.groupby('account_id').cumcount() + 1
    
    return df