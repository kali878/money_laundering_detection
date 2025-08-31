def predict_transaction(txn):
    """
    txn ek dictionary hai ek transaction ka
    Example: {'transaction_id': 'TXN0001', 'amount': 5000, 'transaction_type': 'Transfer'}
    """
    amount = txn["amount"]
    txn_type = txn["transaction_type"]

    # Simple rule
    if amount > 10000 or (txn_type == "Transfer" and amount > 5000):
        return {"transaction_id": txn["transaction_id"], "prediction": "Suspicious"}
    else:
        return {"transaction_id": txn["transaction_id"], "prediction": "Normal"}