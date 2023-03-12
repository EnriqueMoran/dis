import unittest
from unittest.mock import patch, MagicMock
from opendis.RangeCoordinates import GPS
from lib.utils import positionException
from lib.cinematic.cinematicManager import CinematicManager


class TestCinematicManager(unittest.TestCase):
    def setUp(self):
        self.c_manager = CinematicManager()

    def test_set_initial_position(self):
        self.setUp()
        self.c_manager.set_initial_position(23.1234, -110.1234, 10.5)
        self.assertEqual(self.c_manager.initial_pos_x, -2019108.6905351111)
        self.assertEqual(self.c_manager.initial_pos_y, -5510499.341522655)
        self.assertEqual(self.c_manager.initial_pos_z, 2489297.2368305624)
        self.assertEqual(self.c_manager.psi, 1.2195767400990696)
        self.assertEqual(self.c_manager.theta, -1.1672168625392398)
        self.assertEqual(self.c_manager.phi, -3.141592653589793)
        with self.assertRaises(positionException.PositionException):
            self.c_manager.set_initial_position(0, 0, 0)

    def test_set_position(self):
        self.setUp()
        self.c_manager.set_position(54.2677, -80.9858, -40.11)
        self.assertEqual(self.c_manager.pos_x, 584890.6010953691)
        self.assertEqual(self.c_manager.pos_y, -3686939.7127337353)
        self.assertEqual(self.c_manager.pos_z, 5154169.139360829)
        with self.assertRaises(positionException.PositionException):
            self.c_manager.set_position(0, 0, 0)

    def test_set_speed(self):
        self.setUp()
        self.c_manager.set_position(36.497646099124594, -6.185247656271934, 40)
        self.c_manager.set_heading(275)
        self.c_manager.set_speed(10)
        self.assertAlmostEqual(self.c_manager.speed_x, 0.5238608658649963, places=4)
        self.assertAlmostEqual(self.c_manager.speed_y, -5.98775709620677, places=4)
        self.assertAlmostEqual(self.c_manager.speed_z, 7.992016938798407, places=4)

    def test_set_heading(self):
        self.setUp()
        self.c_manager.set_position(23.1234, -110.1234, 10.5)
        self.c_manager.set_heading(90)
        self.assertAlmostEqual(self.c_manager.psi, -0.053588379855596203, places=4)
        self.assertAlmostEqual(self.c_manager.theta, 0.12457754170146115, places=4)
        self.assertAlmostEqual(self.c_manager.phi, 0.041944546942480614, places=4)
    
    def test_set_initial_position_2(self):
        self.setUp()
        set_lat = 12.8497
        set_lon = 102.3284
        set_alt = 410.24
        self.c_manager.set_initial_position(set_lat, set_lon, set_alt)
        get_lat, get_lon, get_alt = self.c_manager.get_initial_position()
        self.assertAlmostEqual(set_lat, get_lat, places=4)
        self.assertAlmostEqual(set_lon, get_lon, places=4)
        self.assertAlmostEqual(set_alt, get_alt, places=4)
    
    def test_set_position_2(self):
        self.setUp()
        set_lat = 46.8519
        set_lon = 56.6933
        set_alt = 29.9301
        self.c_manager.set_position(set_lat, set_lon, set_alt)
        get_lat, get_lon, get_alt = self.c_manager.get_position()
        self.assertAlmostEqual(set_lat, get_lat, places=4)
        self.assertAlmostEqual(set_lon, get_lon, places=4)
        self.assertAlmostEqual(set_alt, get_alt, places=4)
    
    def test_set_heading_2(self):
        self.setUp()
        set_lat = 64.6062
        set_lon = 4.0266
        set_alt = -29.1341
        set_heading = 312.08
        self.c_manager.set_position(set_lat, set_lon, set_alt)
        self.c_manager.set_heading(set_heading)
        get_heading = self.c_manager.get_heading()
        self.assertAlmostEqual(set_heading, get_heading, places=4)
    
    def test_set_speed_2(self):
        self.setUp()
        set_lat = 64.6062
        set_lon = 4.0266
        set_alt = -29.1341
        set_heading = 105.2314
        set_speed = 223.3143
        self.c_manager.set_position(set_lat, set_lon, set_alt)
        self.c_manager.set_heading(set_heading)
        self.c_manager.set_speed(set_speed)
        get_speed = self.c_manager.get_speed()
        self.assertAlmostEqual(set_speed, get_speed, places=4)