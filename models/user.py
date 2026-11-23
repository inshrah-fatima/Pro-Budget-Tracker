from models.budget import Budget
from models.goal import Goal

class User:
    def __init__(self, username: str, currency: str = "PKR"):
        self._username = username
        self._currency = currency
        self._transactions = []
        self._budgets = {}
        self._goals = []

    @property
    def username(self):
        return self._username
        
    @property
    def currency(self):
        return self._currency

    @property
    def transactions(self):
        return self._transactions
        
    @property
    def budgets(self):
        return self._budgets
        
    @property
    def goals(self):
        return self._goals

    def add_transaction(self, transaction):
        self._transactions.append(transaction)

    def set_budget(self, category: str, limit: float):
        self._budgets[category] = Budget(category, limit)
        
    def add_goal(self, goal: Goal):
        self._goals.append(goal)

    def get_balance(self):
        return sum(t.apply() for t in self._transactions)
