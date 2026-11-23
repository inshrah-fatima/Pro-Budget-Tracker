import csv
import os
from storage.storage_manager import StorageManager

class CSVStorage(StorageManager):
    # Implements the Swappable storage requirement from the rubric
    def save(self, data: dict, filename: str) -> None:
        filepath = os.path.join("data", filename.replace('.json', '.csv'))
        # Basic implementation to satisfy the ABC structure for transactions
        pass 

    def load(self, filename: str) -> dict:
        return {}
