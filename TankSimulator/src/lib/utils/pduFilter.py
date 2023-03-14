class PduFilter:

    def __init__(self, exercise, app, site):
        self.exercise = exercise
        self.app = app
        self.site = site
    
    def __eq__(self, other):
        return other.exercise == self.exercise and other.app == self.app and other.site == self.site