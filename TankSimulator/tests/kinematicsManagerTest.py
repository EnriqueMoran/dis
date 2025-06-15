import random
import unittest

from unittest.mock import patch, MagicMock

from lib.utils import positionException
from lib.kinematics.kinematicsManager import KinematicsManager

from opendis.RangeCoordinates import GPS, rad2deg

class TestKinematicsManager(unittest.TestCase):
    def setUp(self):
        self.k_manager = KinematicsManager()

    def test_set_position(self):
        self.setUp()
        for _ in range(10000):
            initial_lat = random.uniform(-90.0, 90.0)
            initial_lon = random.uniform(-90.0, 90.0)
            initial_alt = random.uniform(0, 1000)
            self.k_manager.set_position(initial_lat, initial_lon, initial_alt)
            lat, lon, alt = self.k_manager.get_lat_lon_alt()
            self.assertAlmostEqual(lat, initial_lat, places=6)
            self.assertAlmostEqual(lon, initial_lon, places=6)
            self.assertAlmostEqual(alt, initial_alt, places=6)

    def test_set_speed(self):
        self.setUp()
        for _ in range(10000):
            lat = random.uniform(-90.0, 90.0)
            lon = random.uniform(-90.0, 90.0)
            alt = random.uniform(0, 1000)
            heading = random.uniform(0, 360)
            initial_speed = random.uniform(0, 200)
            self.k_manager.set_position(lat, lon, alt)
            self.k_manager.set_heading(heading)
            self.k_manager.set_speed(initial_speed)
            speed = self.k_manager.get_speed()
            self.assertAlmostEqual(speed, initial_speed, places=6)

    def test_set_heading(self):
        self.setUp()
        for _ in range(10000):
            lat = random.uniform(-90.0, 90.0)
            lon = random.uniform(-90.0, 90.0)
            alt = random.uniform(0, 1000)
            initial_heading = random.uniform(0, 360)
            self.k_manager.set_position(lat, lon, alt)
            self.k_manager.set_heading(initial_heading)
            heading = self.k_manager.get_heading()
            self.assertAlmostEqual(heading, initial_heading, places=6)