class PduFilter:

    def __init__(self, exercise: int, app: int, site: int) -> None:
        self.exercise = exercise
        self.app = app
        self.site = site
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, PduFilter) and other.exercise == self.exercise and other.app == self.app and other.site == self.site