"""TBD"""

import logging
import multicastManager

from opendis.dis7 import StartResumePdu, StopFreezePdu

__author__ = "EnriqueMoran"

logger = logging.getLogger("Main")

class SimulationManager():
    """TBD"""
    def __init__(self, exercise_id=1, application_id=1, site_id=1, simulation_time=1000):
        self.exercise_id = exercise_id
        self.application_id = application_id
        self.site_id = site_id
        self.simulation_time = simulation_time
        self.multicast_manager = multicastManager.MulticastManager()

    def start_resume_simulation(self):
        """TBD"""
        pdu = StartResumePdu()
        pdu.exerciseID = self.exercise_id
        pdu.originatingEntityID.applicationID = self.application_id
        pdu.originatingEntityID.siteID = self.site_id
        pdu.protocolFamily = 0

        self.multicast_manager.send_pdu(pdu)
        logger.info("StartResumePDU sent to %s:%d - exercise_id: %d, application_id: %d, site_id: %d",\
                    self.multicast_manager.multicast_group, self.multicast_manager.multicast_port,\
                    pdu.exerciseID, pdu.originatingEntityID.applicationID,\
                    pdu.originatingEntityID.siteID)

    def pause_simulation(self):
        """TBD"""
        pdu = StopFreezePdu()
        pdu.exerciseID = self.exercise_id
        pdu.originatingEntityID.applicationID = self.application_id
        pdu.originatingEntityID.siteID = self.site_id
        pdu.reason = 1
        pdu.frozenBehavior = 1
        self.multicast_manager.send_pdu(pdu)
        logger.info("StopFreezePDU sent to %s:%d - exercise_id: %d, application_id: %d, site_id: %d",\
                    self.multicast_manager.multicast_group, self.multicast_manager.multicast_port,\
                    pdu.exerciseID, pdu.originatingEntityID.applicationID,\
                    pdu.originatingEntityID.siteID)

    def stop_simulation(self):
        """TBD"""
        pdu = StopFreezePdu()
        pdu.exerciseID = self.exercise_id
        pdu.originatingEntityID.applicationID = self.application_id
        pdu.originatingEntityID.siteID = self.site_id
        pdu.reason = 2
        pdu.frozenBehavior = 4
        self.multicast_manager.send_pdu(pdu)
        logger.info("StopFreezePDU sent to %s:%d - exercise_id: %d, application_id: %d, site_id: %d",\
                    self.multicast_manager.multicast_group, self.multicast_manager.multicast_port,\
                    pdu.exerciseID, pdu.originatingEntityID.applicationID,\
                    pdu.originatingEntityID.siteID)
