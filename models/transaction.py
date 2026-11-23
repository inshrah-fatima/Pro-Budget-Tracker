from abc import ABC, abstractmethod

class Transaction(ABC):
    def __init__(self, amount: float, category: str, date: str, payment_type: str):
        self._amount = amount
        self._category = category
        self._date = date
        self._payment_type = payment_type

    @property
    def amount(self):
        return self._amount

    @property
    def category(self):
        return self._category
        
    @property
    def date(self):
        return self._date
        
    @property
    def payment_type(self):
        return self._payment_type

    @abstractmethod
    def apply(self) -> float:
        pass

    @abstractmethod
    def __str__(self):
        pass
    
    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "amount": self._amount,
            "category": self._category,
            "date": self._date,
            "payment_type": self._payment_type
        }
