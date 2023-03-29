import configparser
import logging

import lib.multicastManager as multicastManager
import lib.exerciseManager as exerciseManager

__author__ = "EnriqueMoran"

class ExerciseDataModel:
    def __init__(self):
        self.exercise_id = 0
        self.application_id = 0
        self.site_id = 0
        self.multicast_group = '0.0.0.0'
        self.multicast_port = 3000
        self.multicast_iface = '0.0.0.0'
        self.ttl = 1
        self.exercise_manager = None
        self.initialize()
    
    def read_config(self):
        """TBD"""
        config = configparser.ConfigParser(inline_comment_prefixes=";")
        config.read("config.ini")

        self.exercise_id = int(config.get("IDENTITY", 'exercise_id'))
        self.application_id = int(config.get("IDENTITY", 'application_id'))
        self.site_id = int(config.get("IDENTITY", 'site_id'))

        self.multicast_group = str(config.get("CONNECTION", 'multicast_group'))
        self.multicast_port = int(config.get("CONNECTION", 'multicast_port'))
        self.multicast_iface = str(config.get("CONNECTION", 'multicast_iface'))
        self.ttl = int(config.get("CONNECTION", 'ttl'))
    
    def initialize(self):
        """TBD"""
        self.read_config()
        self.exercise_manager = exerciseManager.ExerciseManager(self.exercise_id,
                                                                  self.application_id,
                                                                  self.site_id)
        multicast_manager = multicastManager.MulticastManager(self.multicast_group,
                                                                self.multicast_port,
                                                                self.multicast_iface,
                                                                self.ttl)
        self.exercise_manager.multicast_manager = multicast_manager
        self.exercise_manager.multicast_manager.create_connection()
    
    def start_exercise(self):
        """TBD"""
        self.exercise_manager.start_resume_exercise()

    def resume_exercise(self):
        """TBD"""
        self.exercise_manager.start_resume_exercise()

    def pause_exercise(self):
        """TBD"""
        self.exercise_manager.pause_exercise()

    def stop_exercise(self):
        """TBD"""
        self.exercise_manager.stop_exercise()
    
    def get_exercise_time(self):
        milliseconds = self.exercise_manager.exercise_time * 1000
        seconds,_ = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
