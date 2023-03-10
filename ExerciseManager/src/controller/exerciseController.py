class ExerciseController:

    def __init__(self, data_model, view):
        self.data_model = data_model
        self.view = view
    
    def start_exercise(self):
        self.data_model.start_exercise()

    def resume_exercise(self):
        self.data_model.resume_exercise()
    
    def pause_exercise(self):
        self.data_model.pause_exercise()
    
    def stop_exercise(self):
        self.data_model.stop_exercise()
    
    def get_exercise_time(self):
        return self.data_model.get_exercise_time()
    
    def get_exercise_status(self):
        return self.data_model.exercise_manager.get_exercise_status().to_string()
