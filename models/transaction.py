import datetime

class Transaction:
    def __init__(self, description, amount, transaction_type):
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.description = description
        self.amount = amount
        self.type = transaction_type
