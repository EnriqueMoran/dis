"""TBD"""
import logging
import os
import sys
import tests

from lib.core import systemsManager


__author__ = "EnriqueMoran"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                            level=os.environ.get("LOGLEVEL", "INFO"))

logger = logging.getLogger("Main")

class MainApp:

    def __init__(self):
        """TBD"""
        self.systems_manager = systemsManager.SystemsManager()
    
    def run(self):
        pass

if __name__ == "__main__":
    app = MainApp()
    app.run()
    
    sim_sys = app.systems_manager.simulation_system
    sim_sys.read_config()
    sim_sys.listen_to_pdu()
    
    if False:
        test.run_cinematic_tests()