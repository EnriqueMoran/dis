"""TBD"""
import logging
import os
import sys
import tests

from lib.core import systemsManager

__author__ = "EnriqueMoran"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s::%(funcName)s - %(message)s',
                            level=os.environ.get("LOGLEVEL", "DEBUG"))

logger = logging.getLogger("Main")

class MainApp:

    def __init__(self):
        """TBD"""
        self.systems_manager = systemsManager.SystemsManager()
    
    def run(self):
        self.systems_manager.run()

if __name__ == "__main__":
    run_test = False    # Set to True to run unit tests
    if run_test:
        tests.run_kinematics_tests()
    else:
        app = MainApp()
        app.run()