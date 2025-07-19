"""This class is responsible for managing all the systems that constitute and define the operation of the tank."""

import threading
import time

from lib.kinematics import kinematicsManager
from lib.entity import entityManager
from lib.fuel import fuelManager
from lib.simulation import simulationManager

class SystemsManager:

    def __init__(self):
        self.entity_system = entityManager.EntityManager()
        self.fuel_system = fuelManager.FuelManager()
        self.kinematics_system = kinematicsManager.KinematicsManager()
        self.simulation_system = simulationManager.SimulationManager(self.kinematics_system)
        self.weapon_system = None
        self.comm_system = None
        self.sensors_system = None
        self.electric_system = None
        self.physic_system = None

        self.exercise_time = 0    # Exercise time in ms
        self.simulation_freq = 1000    # ms
        self.execution_thread = None

    def __del__(self):
        if self.execution_thread:
            self.execution_thread.join()
    
    def _simulation_tick(self):
        while True:
            if self.simulation_system.exercise_status == simulationManager.ExerciseStatus.RUNNING:
                self.exercise_time += 1
                time.sleep(self.simulation_freq / 1000)
            elif self.simulation_system.exercise_status == simulationManager.ExerciseStatus.TERMINATED:
                self.entity_system.reset_data()
                self.fuel_system.reset_fuel()
                self.exercise_time = 0

    def run(self):
        self.simulation_system.listen_to_pdu()
        self.execution_thread = threading.Thread(target=self._simulation_tick)
        self.execution_thread.start()
