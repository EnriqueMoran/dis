"""TBD"""

import configparser

__author__ = "EnriqueMoran"

from opendis.dis7 import EngineFuel, EngineFuelReload

class FuelManager:

    def __init__(self) -> None:
        self.engine_fuel = EngineFuel()
        self.engine_fuel.fuelMeasurementUnits = 1         # Liter
        self.engine_fuel.fuelType = 2                     # Diesel fuel
        self.engine_fuel_reload = EngineFuelReload()
        self.engine_fuel_reload.fuelMeasurementUnits = 1  # Liter
        self._consumption_rate = 0                        # Liters per km
        self.initial_fuel_quantity = 0                    # Liter
        self.read_config()

    def read_config(self) -> None:
        """
        Read and process configuration file.
        """
        config = configparser.ConfigParser(inline_comment_prefixes=";")
        config.read("config.ini")

        self.initial_fuel_quantity = float(config.get("FUEL", 'capacity'))
        self.engine_fuel.fuelQuantity = self.initial_fuel_quantity
        self.engine_fuel_reload.maximumQuantity = float(config.get("FUEL", 'capacity'))
        self.engine_fuel_reload.maximumQuantityReloadTime = float(config.get("FUEL",
                                                                             'capacity_reload_time'))
        self._consumption_rate = float(config.get("FUEL", 'consumption_rate'))
        self.engine_fuel_reload.standardQuantity = self.engine_fuel_reload.maximumQuantity
        self.engine_fuel_reload.standardQuantityReloadTime = self.engine_fuel_reload.maximumQuantityReloadTime

    def process_fuel_consumption(self, distance_traveled: float) -> None:
        """
        :params distance_traveled: distance traveled in meters.
        """
        consumed_fuel = self._consumption_rate * (distance_traveled / 1000)
        remaining_fuel = self.engine_fuel.fuelQuantity - consumed_fuel
        self.engine_fuel.fuelQuantity = remaining_fuel if remaining_fuel >= 0 else 0
    
    def add_fuel(self, fuel_quantity: float) -> float:
        """
        Return the excess of fuel.
        """
        excess_fuel = 0
        self.engine_fuel.fuelQuantity += fuel_quantity
        if self.engine_fuel.fuelQuantity > self.engine_fuel_reload.maximumQuantity:
            excess_fuel = self.engine_fuel.fuelQuantity - self.engine_fuel_reload.maximumQuantity
            self.engine_fuel.fuelQuantity = self.engine_fuel_reload.maximumQuantity
        return excess_fuel
    
    def reset_fuel(self) -> None:
        self.engine_fuel.fuelQuantity = self.initial_fuel_quantity