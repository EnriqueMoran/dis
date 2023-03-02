"""TBD"""

import configparser
import logging
import os
import time

import multicastManager
import simulationManager

EXERCISE_ID = 1
APPLICATION_ID = 1
SITE_ID = 1
SIMULATION_TIME = 1000

MULTICAST_GROUP = '0.0.0.0'
MULTICAST_PORT = 3000
MULTICAST_IFACE = '0.0.0.0'
TTL = 2

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
                            level=os.environ.get("LOGLEVEL", "INFO"))

logger = logging.getLogger("Main")

def read_config():
    """TBD"""
    global EXERCISE_ID, APPLICATION_ID, SITE_ID, SIMULATION_TIME, MULTICAST_GROUP, \
        MULTICAST_PORT, MULTICAST_IFACE, TTL

    config = configparser.ConfigParser()
    config.read("config.ini")

    EXERCISE_ID = int(config.get("SIMULATION", 'exercise_id'))
    APPLICATION_ID = int(config.get("SIMULATION", 'application_id'))
    SITE_ID = int(config.get("SIMULATION", 'site_id'))
    SIMULATION_TIME = int(config.get("SIMULATION", 'simulation_time'))

    MULTICAST_GROUP = str(config.get("CONNECTION", 'multicast_group'))
    MULTICAST_PORT = int(config.get("CONNECTION", 'multicast_port'))
    MULTICAST_IFACE = str(config.get("CONNECTION", 'multicast_iface'))
    TTL = int(config.get("CONNECTION", 'ttl'))

    logger.info("Configuration successfully loaded.")
    logger.info("exercise_id: %d, application_id: %d, site_id: %d, simulation_time: %d",
                EXERCISE_ID, APPLICATION_ID, SITE_ID, SIMULATION_TIME)
    logger.info("multicast_group: %s, multicast_port: %d, multicast_iface: %s, ttl: %d", \
                MULTICAST_GROUP, MULTICAST_PORT, MULTICAST_IFACE, TTL)

def start_simulation():
    """TBD"""
    simulation_manager = simulationManager.SimulationManager()
    multicast_manager = multicastManager.MulticastManager(MULTICAST_GROUP, MULTICAST_PORT,
                                                          MULTICAST_IFACE, TTL)
    simulation_manager.multicast_manager = multicast_manager
    simulation_manager.multicast_manager.create_connection()
    simulation_manager.start_resume_simulation()
    logger.info("Simulation started.")

def resume_simulation():
    """TBD"""
    simulation_manager = simulationManager.SimulationManager()
    multicast_manager = multicastManager.MulticastManager(MULTICAST_GROUP, MULTICAST_PORT,
                                                          MULTICAST_IFACE, TTL)
    simulation_manager.multicast_manager = multicast_manager
    simulation_manager.multicast_manager.create_connection()
    simulation_manager.start_resume_simulation()
    logger.info("Simulation resumed.")

def pause_simulation():
    """TBD"""
    simulation_manager = simulationManager.SimulationManager()
    multicast_manager = multicastManager.MulticastManager(MULTICAST_GROUP, MULTICAST_PORT,
                                                          MULTICAST_IFACE, TTL)
    simulation_manager.multicast_manager = multicast_manager
    simulation_manager.multicast_manager.create_connection()
    simulation_manager.pause_simulation()
    logger.info("Simulation paused.")

def stop_simulation():
    """TBD"""
    simulation_manager = simulationManager.SimulationManager()
    multicast_manager = multicastManager.MulticastManager(MULTICAST_GROUP, MULTICAST_PORT,
                                                          MULTICAST_IFACE, TTL)
    simulation_manager.multicast_manager = multicast_manager
    simulation_manager.multicast_manager.create_connection()
    simulation_manager.stop_simulation()
    logger.info("Simulation terminated.")

def run():
    """TBD"""
    read_config()
    start_simulation()
    time.sleep(1)
    pause_simulation()
    time.sleep(1)
    resume_simulation()
    time.sleep(1)
    stop_simulation()
    while True:
        time.sleep(1)
        stop_simulation()


if __name__ == "__main__":
    run()
