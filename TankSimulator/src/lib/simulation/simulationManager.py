import configparser
import datetime
import json
import logging
import threading
import time

from enum import Enum

from lib.entity import entityManager

from lib.simulation.communication import multicastManager
from lib.utils.pduFilter import PduFilter

from opendis.dis7 import EntityStatePdu
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

    def __init__(self, kinematics_system=None):
        self.exercise_time = 0
        self.exercise_status = ExerciseStatus.UNINITIALIZED
        self.multicast_manager = None
        self.recv_pdu_thread = None
        self.send_pdu_thread = None
        self.message_frequency = 0
        self.exercise_id = 0
        self.application_id = 0
        self.site_id = 0
        self.entity_id = 0
        self.pdu_filter_list = []
        self.kinematics_system = kinematics_system
        self._data_initialized = False    # Set to True when received ESPDU for the first time
        self.read_config()
        self.listen_to_pdu()
        self.emit_entity_pdus()

    def __del__(self):
        if self.recv_pdu_thread:
            self.recv_pdu_thread.join()
        if self.send_pdu_thread:
            self.send_pdu_thread.join()

    def read_config(self):
        """
        Read and process configuration file.
        """
        config = configparser.ConfigParser(inline_comment_prefixes=";")
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
        self.message_frequency = float(config.get("CONNECTION", 'message_frequency'))

        self.exercise_id = int(config.get("IDENTITY", 'exercise_id'))
        self.application_id = int(config.get("IDENTITY", 'application_id'))
        self.site_id = int(config.get("IDENTITY", 'site_id'))
        self.entity_id = int(config.get("IDENTITY", 'entity_id'))

        self.multicast_manager = multicastManager.MulticastManager(multicast_group, multicast_port,
                                                                   multicast_iface, ttl)
        self.multicast_manager.create_connection()
        self.multicast_manager.add_listener(self)

    def listen_to_pdu(self):
        self.recv_pdu_thread = threading.Thread(target=self.multicast_manager.receive_pdu)
        self.recv_pdu_thread.start()
    
    def emit_entity_pdus(self):
        """
        Initialize ESPDU emitting thread.
        """
        self.send_pdu_thread = threading.Thread(target=self.send_entity_pdus)
        self.send_pdu_thread.start()
    
    def send_entity_pdus(self):
        """
        Send ESPDU periodically.
        """
        while True:
            if self.exercise_status == ExerciseStatus.RUNNING:
                if self._data_initialized:
                    self.send_entity_state_pdu()
            time.sleep(1 / self.message_frequency)

    def on_pdu_received(self, pdu):
        if self.can_process_pdu(pdu):
            logger.debug("Processing %s", pdu.__class__.__name__)
            if PduTypeDecoders[pdu.pduType] == PduTypeDecoders[13]:      # PduTypeDecoders.StartResumePdu
                self.exercise_status = ExerciseStatus.RUNNING
                logger.info("Simulation Running")
            elif PduTypeDecoders[pdu.pduType] == PduTypeDecoders[14]:    # PduTypeDecoders.StopFreezePdu
                logger.debug("frozenBehavior: %d, reason: %d", pdu.frozenBehavior, pdu.reason)
                if pdu.reason == 2:    # Exercise termination
                    self.exercise_status = ExerciseStatus.TERMINATED
                    self._data_initialized = False
                    logger.info("Simulation Terminated")
                elif pdu.frozenBehavior == 1:    # Stop transmitting PDUs
                    self.exercise_status = ExerciseStatus.PAUSED
                    logger.info("Simulation Paused")
            elif PduTypeDecoders[pdu.pduType] == PduTypeDecoders[1]:     # PduTypeDecoders.EntityStatePdu
                if pdu.entityID.entityID == self.entity_id:    # Own entity
                    entityManager.EntityManager().set_data(pdu)
                    self._data_initialized = True

    def can_process_pdu(self, pdu):
        """
        Return True if pdu can be processed, False otherwise.
        """
        pdu_exercise = pdu.exerciseID
        pdu_app = -1
        pdu_site = -1
        has_originatingEntityID = [PduTypeDecoders[13], PduTypeDecoders[14]]
        has_entityID = [PduTypeDecoders[1]]
        if PduTypeDecoders[pdu.pduType] in has_originatingEntityID:
            pdu_app = pdu.originatingEntityID.applicationID
            pdu_site = pdu.originatingEntityID.siteID
        elif PduTypeDecoders[pdu.pduType] in has_entityID:
            pdu_app = pdu.entityID.applicationID
            pdu_site = pdu.entityID.siteID
        pdu_filter = PduFilter(pdu_exercise, pdu_app, pdu_site)
        can_be_processed = pdu_filter in self.pdu_filter_list
        logger.debug("Received PDU (%s) - exercise_id: %d, application_id: %d, site_id: %d",\
                        pdu.__class__.__name__, pdu_exercise, pdu_app,pdu_site)
        if can_be_processed:
            logger.debug("PDU matches filters, will be processed.")
        else:
            logger.debug("PDU does not match filters, won't be processed.")
        return can_be_processed

    def send_entity_state_pdu(self):
        entity_system = entityManager.EntityManager()    # Singleton
        pdu = EntityStatePdu()
        pdu.exerciseID = self.exercise_id
        pdu.entityID.siteID = self.site_id
        pdu.entityID.applicationID = self.application_id
        pdu.timestamp = int(datetime.datetime.now().timestamp())
        pdu.capabilities = entity_system.get_capabilities()
        pdu.deadReckoningParameters = entity_system.get_dead_reckoning_params()
        pdu.entityAppearance = entity_system.get_entity_appearance()
        pdu.entityID.entityID = entity_system.get_entity_id()
        pdu.entityLinearVelocity = entity_system.get_entity_linear_velocity()
        pdu.entityLocation = entity_system.get_entity_location()
        pdu.entityOrientation = entity_system.get_entity_orientation()
        pdu.entityType = entity_system.get_entity_type()
        pdu.forceId = entity_system.get_force_id()
        pdu.marking = entity_system.get_marking()
        pdu.numberOfVariableParameters = entity_system.get_number_of_variable_parameters()
        pdu.variableParameters = entity_system.get_variable_parameters()

        log_message = "\t"*1 + f"exerciseID: {pdu.exerciseID} \n"+"\t"*1 + \
                      f"siteID: {pdu.entityID.siteID} \n"+"\t"*1 + \
                      f"applicationID: {pdu.entityID.applicationID} \n"+"\t"*1 + \
                      f"entityID: {pdu.entityID.entityID} \n"+"\t"*1 + \
                      f"timestamp: {pdu.timestamp} \n"+"\t"*1 + \
                      f"capabilities: {pdu.capabilities} \n"+"\t"*1 + \
                      f"deadReckoningParameters: \n"+"\t"*2 + \
                      f"deadReckoningAlgorithm: {pdu.deadReckoningParameters.deadReckoningAlgorithm} \n"+"\t"*2 + \
                      f"parameters: {pdu.deadReckoningParameters.parameters} \n"+"\t"*1 + \
                      f"entityLinearAcceleration: \n"+"\t"*2 + \
                      f"x: {pdu.deadReckoningParameters.entityLinearAcceleration.x} \n"+"\t"*2 + \
                      f"y: {pdu.deadReckoningParameters.entityLinearAcceleration.y} \n"+"\t"*2 + \
                      f"z: {pdu.deadReckoningParameters.entityLinearAcceleration.z} \n"+"\t"*1 + \
                      f"entityAngularVelocity: \n"+"\t"*2 + \
                      f"x: {pdu.deadReckoningParameters.entityAngularVelocity.x} \n"+"\t"*2 + \
                      f"y: {pdu.deadReckoningParameters.entityAngularVelocity.y} \n"+"\t"*2 + \
                      f"z: {pdu.deadReckoningParameters.entityAngularVelocity.z} \n"+"\t"*1 + \
                      f"entityAppearance: {pdu.entityAppearance} \n"+"\t"*1 + \
                      f"entityLinearVelocity: \n"+"\t"*2 + \
                      f"x: {pdu.entityLinearVelocity.x} \n"+"\t"*2 + \
                      f"y: {pdu.entityLinearVelocity.y} \n"+"\t"*2 + \
                      f"z: {pdu.entityLinearVelocity.z} \n"+"\t"*1 + \
                      f"entityLocation: \n"+"\t"*2 + \
                      f"x: {pdu.entityLocation.x} \n"+"\t"*2 + \
                      f"y: {pdu.entityLocation.y} \n"+"\t"*2 + \
                      f"z: {pdu.entityLocation.z} \n"+"\t"*1 + \
                      f"entityOrientation: \n"+"\t"*2 + \
                      f"psi: {pdu.entityOrientation.psi} \n"+"\t"*2 + \
                      f"theta: {pdu.entityOrientation.theta} \n"+"\t"*2 + \
                      f"phi: {pdu.entityOrientation.phi} \n"+"\t"*1 + \
                      f"entityType: \n"+"\t"*1 + \
                      f"entityKind : {pdu.entityType.entityKind} \n"+"\t"*2 + \
                      f"domain : {pdu.entityType.domain} \n"+"\t"*2 + \
                      f"country : {pdu.entityType.country} \n"+"\t"*2 + \
                      f"category : {pdu.entityType.category} \n"+"\t"*2 + \
                      f"subcategory : {pdu.entityType.subcategory} \n"+"\t"*2 + \
                      f"specific : {pdu.entityType.specific} \n"+"\t"*2 + \
                      f"extra : {pdu.entityType.extra} \n"+"\t"*1 + \
                      f"forceId: {pdu.forceId} \n"+"\t"*1 + \
                      f"marking: {pdu.marking.characters} \n"+"\t"*2 + \
                      f"numberOfVariableParameters: {pdu.numberOfVariableParameters} \n"+"\t"*2 + \
                      f"variableParameters: {pdu.variableParameters}"
        self.multicast_manager.send_pdu(pdu)
        logger.debug("EntityStatePDU sent: \n%s", log_message)
