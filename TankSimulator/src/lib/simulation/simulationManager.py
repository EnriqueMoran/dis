import configparser
import json
import logging
import threading

from lib.simulation.communication import multicastManager
from lib.utils.pduFilter import PduFilter

from opendis.PduFactory import createPdu, PduTypeDecoders 

__author__ = "EnriqueMoran"

logger = logging.getLogger("Main")

class SimulationManager:

    def __init__(self):
        self.multicast_manager = None
        self.recv_pdu_thread = None
        self.pdu_filter_list = []
    
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
            if PduTypeDecoders[pdu.pduType] == PduTypeDecoders[13]:    # PduTypeDecoders.StartResumePdu
                logger.info("Processing %s:", pdu.__class__.__name__)

                
    
    
    def process_pdu(self, pdu):
        """
        Return True if pdu can be processed, False otherwise.
        """
        pdu_exercise = pdu.exerciseID
        pdu_app = pdu.originatingEntityID.applicationID
        pdu_site = pdu.originatingEntityID.siteID
        pdu_filter = PduFilter(pdu_exercise, pdu_app, pdu_site)
        logger.debug("Received PDU (%s) - exercise_id: %d, application_id: %d, site_id: %d",\
                        pdu.__class__.__name__, pdu_exercise, pdu_app,pdu_site)
        can_be_processed = pdu_filter in self.pdu_filter_list
        if can_be_processed:
            logger.debug("PDU matches filtered {exercise, application, site}, will be processed.")
        else:
            logger.debug("PDU does not match filtered {exercise, application, site}, won't " + \
                        "be processed.")
        return pdu_filter in self.pdu_filter_list
    

  