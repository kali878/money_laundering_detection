import unittest
import pandas as pd
from src.detector import detect_patterns
from src.patterns import smurfing_pattern, layering_pattern

class TestDetector(unittest.TestCase):
    def setUp(self):
        self.smurf_df = pd.DataFrame({
            'transaction_id': range(1, 12),
            'account_id': [1]*11,
            'amount': [500]*11,
            'timestamp': pd.date_range(start='2025-01-01', periods=11, freq='D'),
            'kyc_verified': [True]*11,
            'time_delta': [0]*11
        })
        
        self.layer_df = pd.DataFrame({
            'transaction_id': range(1, 7),
            'account_id': [2]*6,
            'amount': [2000]*6,
            'timestamp': pd.date_range(start='2025-01-01', periods=6, freq='10min'),
            'kyc_verified': [False]*6,
            'time_delta': [10]*6
        })

    def test_smurfing(self):
        self.assertTrue(smurfing_pattern(self.smurf_df))

    def test_layering(self):
        self.assertTrue(layering_pattern(self.layer_df))

if __name__ == "__main__":
    unittest.main()