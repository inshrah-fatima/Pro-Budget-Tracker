from models.transaction import Transaction

class Income(Transaction):
    def __init__(self, amount: float, category: str, date: str, payment_type: str):
        super().__init__(amount, category, date, payment_type)

    def apply(self) -> float:
        return self.amount

    def __str__(self):
        return f"+{self.amount} ({self.category})"
