import random
import unittest

from unittest.mock import patch, MagicMock

from lib.utils import positionException
from lib.cinematic.cinematicManager import CinematicManager

from opendis.RangeCoordinates import GPS, rad2deg

class TestCinematicManager(unittest.TestCase):
    def setUp(self):
        self.c_manager = CinematicManager()

    def test_set_position(self):
        self.setUp()
        for _ in range(10000):
            initial_lat = random.uniform(-90.0, 90.0)
            initial_lon = random.uniform(-90.0, 90.0)
            initial_alt = random.uniform(0, 1000)
            self.c_manager.set_position(initial_lat, initial_lon, initial_alt)
            lat, lon, alt = self.c_manager.get_lat_lon_alt()
            self.assertAlmostEqual(rad2deg(lat), initial_lat, places=4)
            self.assertAlmostEqual(rad2deg(lon), initial_lon, places=4)
            self.assertAlmostEqual(alt, initial_alt, places=4)

    def test_set_speed(self):
        self.setUp()
        for _ in range(10000):
            lat = random.uniform(-90.0, 90.0)
            lon = random.uniform(-90.0, 90.0)
            alt = random.uniform(0, 1000)
            heading = random.uniform(0, 360)
            initial_speed = random.uniform(0, 200)
            self.c_manager.set_position(lat, lon, alt)
            self.c_manager.set_heading(heading)
            self.c_manager.set_speed(initial_speed)
            speed = self.c_manager.get_speed()
            self.assertAlmostEqual(speed, initial_speed, places=4)

    def test_set_heading(self):
        self.setUp()
        for _ in range(10000):
            lat = random.uniform(-90.0, 90.0)
            lon = random.uniform(-90.0, 90.0)
            alt = random.uniform(0, 1000)
            initial_heading = random.uniform(0, 360)
            self.c_manager.set_position(lat, lon, alt)
            self.c_manager.set_heading(initial_heading)
            heading = self.c_manager.get_heading()
            self.assertAlmostEqual(heading, initial_heading, places=4)