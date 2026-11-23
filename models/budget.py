class Budget:
    def __init__(self, category: str, limit: float):
        self._category = category
        self._limit = limit

    @property
    def limit(self):
        return self._limit
