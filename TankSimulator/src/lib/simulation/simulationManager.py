import configparser
import json
import logging
import threading

from enum import Enum

from lib.simulation.communication import multicastManager
from lib.utils.pduFilter import PduFilter

from opendis.PduFactory import PduTypeDecoders 

__author__ = "EnriqueMoran"

logger = logging.getLogger("SimulationManager")

class ExerciseStatus(Enum):
    UNINITIALIZED = 0
    RUNNING = 1
    PAUSED = 2
    TERMINATED = 3

    def to_string(self):
        return self.name

class SimulationManager:

    def __init__(self):
        self.exercise_time = 0
        self.exercise_status = ExerciseStatus.UNINITIALIZED
        self.multicast_manager = None
        self.recv_pdu_thread = None
        self.pdu_filter_list = []
        self.read_config()

    def __del__(self):
        if self.recv_pdu_thread:
            self.recv_pdu_thread.join()

    def read_config(self):
        """
        Read and process configuration file.
        """
        config = configparser.ConfigParser()
        config.read("config.ini")
        pdu_filter_path = config.get('FILES', 'pdu_filter_path')
        with open(pdu_filter_path, 'r') as f:
            allowed_pdu = json.load(f)
            for item in allowed_pdu:
                exercise_id = item['exercise_id']
                application_id = item['application_id']
                site_id = item['site_id']
                filter = PduFilter(exercise_id, application_id, site_id)
                self.pdu_filter_list.append(filter)

        multicast_group = str(config.get("CONNECTION", 'multicast_group'))
        multicast_port = int(config.get("CONNECTION", 'multicast_port'))
        multicast_iface = str(config.get("CONNECTION", 'multicast_iface'))
        ttl = int(config.get("CONNECTION", 'ttl'))

        self.multicast_manager = multicastManager.MulticastManager(multicast_group, multicast_port,
                                                                   multicast_iface, ttl)
        self.multicast_manager.create_connection()
        self.multicast_manager.add_listener(self)

    def listen_to_pdu(self):
        self.recv_pdu_thread = threading.Thread(target=self.multicast_manager.receive_pdu)
        self.recv_pdu_thread.start()

    def on_pdu_received(self, pdu):
        if self.process_pdu(pdu):
            logger.debug("Processing %s", pdu.__class__.__name__)
            if PduTypeDecoders[pdu.pduType] == PduTypeDecoders[13]:    # PduTypeDecoders.StartResumePdu
                self.exercise_status = ExerciseStatus.RUNNING
                logger.info("Simulation Running")
            elif PduTypeDecoders[pdu.pduType] == PduTypeDecoders[14]:    # PduTypeDecoders.StopFreezePdu
                logger.debug("frozenBehavior: %d, reason: %d", pdu.frozenBehavior, pdu.reason)
                if pdu.reason == 2:    # Exercise termination
                    self.exercise_status = ExerciseStatus.TERMINATED
                    logger.info("Simulation Terminated")
                elif pdu.frozenBehavior == 1:    # Stop transmitting PDUs
                    self.exercise_status = ExerciseStatus.PAUSED
                    logger.info("Simulation Paused")

    def process_pdu(self, pdu):
        """
        Return True if pdu can be processed, False otherwise.
        """
        pdu_exercise = pdu.exerciseID
        pdu_app = pdu.originatingEntityID.applicationID
        pdu_site = pdu.originatingEntityID.siteID
        pdu_filter = PduFilter(pdu_exercise, pdu_app, pdu_site)
        can_be_processed = pdu_filter in self.pdu_filter_list
        logger.debug("Received PDU (%s) - exercise_id: %d, application_id: %d, site_id: %d",\
                        pdu.__class__.__name__, pdu_exercise, pdu_app,pdu_site)
        if can_be_processed:
            logger.debug("PDU matches filters, will be processed.")
        else:
            logger.debug("PDU does not match filters, won't be processed.")
        return can_be_processed
