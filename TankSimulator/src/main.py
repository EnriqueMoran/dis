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
    
    def _test(self):
        self.systems_manager.cinematic_system.set_position(36.46887579796468, -6.24444889799417, 0)
        self.systems_manager.cinematic_system.set_heading(281)
        self.systems_manager.cinematic_system.set_speed(2.78)
        self.systems_manager.run()

if __name__ == "__main__":
    if False:    # Set to True to run unit tests
        tests.run_cinematic_tests()

    app = MainApp()
    #app.run()
    app._test()