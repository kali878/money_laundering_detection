# src/rules.py

def check_suspicious(transaction):
    """
    transaction: dict {'amount': .., 'country': .., 'account_age': ..}
    return: str ('normal' / 'suspicious')
    """
    if transaction["amount"] > 100000:   # high-value
        return "suspicious"
    if transaction["country"] in ["Iran", "North Korea"]:
        return "suspicious"
    if transaction["account_age"] < 30:  # new account
        return "suspicious"
    return "normal"