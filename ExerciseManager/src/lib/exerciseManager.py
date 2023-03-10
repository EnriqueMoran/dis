"""TBD"""

import logging
import threading
import time

import lib.multicastManager as multicastManager

from enum import Enum
from opendis.dis7 import StartResumePdu, StopFreezePdu


__author__ = "EnriqueMoran"

logger = logging.getLogger("Main")

class ExerciseStatus(Enum):
    UNINITIALIZED = 0
    RUNNING = 1
    PAUSED = 2
    TERMINATED = 3

    def to_string(self):
        return self.name

class ExerciseManager():
    """TBD"""
    def __init__(self, exercise_id=1, application_id=1, site_id=1):
        self.exercise_id = exercise_id
        self.application_id = application_id
        self.site_id = site_id
        self.exercise_time = 0
        self.exercise_status = ExerciseStatus.UNINITIALIZED
        self.multicast_manager = multicastManager.MulticastManager()
        self.time_thread = None
        self.time_lock = threading.Lock()

    def start_resume_exercise(self) -> None:
        """TBD"""
        if self.exercise_status != ExerciseStatus.RUNNING:
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
        
            with self.time_lock:
                if self.exercise_status != ExerciseStatus.PAUSED:
                    self.exercise_time = 0
                self.exercise_status = ExerciseStatus.RUNNING
            self.time_thread = threading.Thread(target=self._time_tick)
            self.time_thread.start()


    def pause_exercise(self) -> None:
        """TBD"""
        if self.exercise_status == ExerciseStatus.RUNNING:
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

            with self.time_lock:
                self.exercise_status = ExerciseStatus.PAUSED
            if self.time_thread:
                self.time_thread.join()
                self.time_thread = None

    def stop_exercise(self) -> None:
        """TBD"""
        if self.exercise_status == ExerciseStatus.RUNNING or self.exercise_status == ExerciseStatus.PAUSED:
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
     
            with self.time_lock:
                self.exercise_status = ExerciseStatus.TERMINATED
            if self.time_thread:
                self.time_thread.join()
                self.time_thread = None
    
    def _time_tick(self) -> None:
        """Increase exercise time every second."""
        while self.exercise_status == ExerciseStatus.RUNNING:
            with self.time_lock:
                self.exercise_time += 1
            time.sleep(1)
    
    def get_exercise_status(self) -> ExerciseStatus:
        return self.exercise_status
