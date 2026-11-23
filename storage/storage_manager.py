from abc import ABC, abstractmethod

class StorageManager(ABC):
    @abstractmethod
    def save(self, data: dict, filename: str) -> None:
        pass

    @abstractmethod
    def load(self, filename: str) -> dict:
        pass
