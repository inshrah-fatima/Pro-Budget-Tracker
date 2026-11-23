import json
import os
from storage.storage_manager import StorageManager

class JSONStorage(StorageManager):
    def save(self, data: dict, filename: str) -> None:
        filepath = os.path.join("data", filename)
        # Yeh line missing folder (data) automatically create kar degi
        os.makedirs(os.path.dirname(filepath), exist_ok=True) 
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self, filename: str) -> dict:
        filepath = os.path.join("data", filename)
        if not os.path.exists(filepath):
            return {}
        with open(filepath, 'r') as f:
            return json.load(f)