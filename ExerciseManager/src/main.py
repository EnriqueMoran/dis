"""TBD"""
import logging
import os
import sys

import tkinter as tk
import controller.exerciseController as Controller
import model.exerciseDataModel as Model
import view.exerciseView as View

__author__ = "EnriqueMoran"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s::%(funcName)s - %(message)s',
                            level=os.environ.get("LOGLEVEL", "DEBUG"))

logger = logging.getLogger("Main")

class MainApp:

    def __init__(self):
        """TBD"""
        self.model = Model.ExerciseDataModel()
        self.view = View.ExerciseView()
        self.controller = Controller.ExerciseController(self.model, self.view)
        self.view.set_controller(self.controller)
    
    def run(self):
        self.view.run()

if __name__ == "__main__":
    app = MainApp()
    app.run()
