class Goal:
    def __init__(self, name: str, target: float, saved: float = 0.0):
        self._name = name
        self._target = target
        self._saved = saved

    @property
    def name(self):
        return self._name

    @property
    def target(self):
        return self._target
        
    @property
    def saved(self):
        return self._saved
        
    @property
    def percentage(self):
        return min((self._saved / self._target) * 100 if self._target > 0 else 0, 100)
