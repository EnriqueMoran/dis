"""This class is responsible for managing all the systems that constitute and define the operation of the tank."""

from lib.cinematic import cinematicManager

class SystemsManager:

    def __init__(self):
        self.simulation_system = None
        self.cinematic_system = cinematicManager.CinematicManager()
        self.fuel_system = None
        self.weapon_system = None
        self.comm_system = None
        self.sensors_system = None
        self.electric_system = None
        self.physic_system = None
    
