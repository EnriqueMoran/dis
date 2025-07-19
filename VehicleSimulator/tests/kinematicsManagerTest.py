import math
import random
import unittest

from opendis.RangeCoordinates import GPS, WGS84

from lib.utils import positionException
from lib.kinematics.kinematicsManager import KinematicsManager


class TestKinematicsManager(unittest.TestCase):
    def __init__(self):
        self.k_manager = KinematicsManager()
    
    def test_set_orientation(self):
        tol_angle = 1e-2  # 0.01°

        for _ in range(10000):
            initial_roll  = random.uniform(-90.0, 90.0)
            initial_pitch = random.uniform(-90.0, 90.0)
            initial_yaw   = random.uniform(0, 1000)

            self.k_manager.set_orientation(initial_roll, initial_pitch, initial_yaw)
            roll, pitch, yaw = self.k_manager.get_roll_pitch_yaw()

            self.assertAlmostEqual(roll, initial_roll, delta=tol_angle)
            self.assertAlmostEqual(pitch, initial_pitch, delta=tol_angle)
            self.assertAlmostEqual(yaw, initial_yaw, delta=tol_angle)

    def test_set_position(self):
        tol_lat_lon = 1e-5   # ~1.1 m
        tol_alt     = 1.5    # 1.5 m

        for _ in range(10000):
            initial_lat = random.uniform(-90.0, 90.0)
            initial_lon = random.uniform(-90.0, 90.0)
            initial_alt = random.uniform(0, 1000)

            self.k_manager.set_position(initial_lat, initial_lon, initial_alt)
            lat, lon, alt = self.k_manager.get_lat_lon_alt()

            self.assertAlmostEqual(lat, initial_lat, delta=tol_lat_lon)
            self.assertAlmostEqual(lon, initial_lon, delta=tol_lat_lon)
            self.assertAlmostEqual(alt, initial_alt, delta=tol_alt)

    def test_set_speed(self):
        tol_speed = 1e-3  # 1 mm/s
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

            self.assertAlmostEqual(speed, initial_speed, delta=tol_speed)

    def test_set_heading(self):
        tol_heading = 1e-3  # 0.001°

        for _ in range(10000):
            lat = random.uniform(-90.0, 90.0)
            lon = random.uniform(-90.0, 90.0)
            alt = random.uniform(0, 1000)
            initial_heading = random.uniform(0, 360)

            self.k_manager.set_position(lat, lon, alt)
            self.k_manager.set_heading(initial_heading)
            heading = self.k_manager.get_heading()

            self.assertAlmostEqual(heading, initial_heading, delta=tol_heading)
    
    def test_process_kinematics(self):
        tol_lat_lon = 1e-5   # ~1.1 m
        tol_alt     = 1.5    # 1.5 m
        tol_angle   = 1e-2   # 0.01°

        for _ in range(10000):
            initial_lat = random.uniform(-90.0, 90.0)
            initial_lon = random.uniform(-90.0, 90.0)
            initial_alt = random.uniform(0, 1000)

            speed   = random.uniform(0, 30.0)
            roll    = random.uniform(-180.0, 180.0)
            pitch   = random.uniform(-90.0,   90.0)
            heading = random.uniform(0.0, 360.0)
            dt      = random.randint(0, 86400)
        
            self.k_manager.set_position(initial_lat, initial_lon, initial_alt)
            self.k_manager.set_orientation(roll, pitch, heading)
            self.k_manager.set_speed(speed)

            old_roll, old_pitch, old_yaw = self.k_manager.get_roll_pitch_yaw()

            self.k_manager.process_kinematics(dt)

            # Calculate new position
            horiz_dist = speed * math.cos(math.radians(pitch)) * dt
            vert_dist  = speed * math.sin(math.radians(pitch)) * dt

            R     = WGS84.a
            arc   = horiz_dist / R
            lat  = math.radians(initial_lat)
            lon  = math.radians(initial_lon)
            heading  = math.radians(heading)

            initial_lat_r = math.radians(initial_lat)
            initial_lon_r = math.radians(initial_lon)
            heading_r = math.radians(heading)

            pred_lat_r = math.asin(math.sin(initial_lat_r)*math.cos(arc) + 
                                   math.cos(initial_lat_r)*math.sin(arc)*math.cos(heading_r))
            
            pred_lon_r = initial_lon_r + math.atan2(
                math.sin(heading_r)*math.sin(arc)*math.cos(initial_lat_r),
                math.cos(arc) - math.sin(initial_lat_r)*math.sin(pred_lat_r))
            
            pred_lat= math.degrees(pred_lat_r)
            pred_lon = math.degrees(pred_lon_r) % 360
            pred_alt = initial_alt + vert_dist

            new_lat, new_lon, new_alt    = self.k_manager.get_lat_lon_alt()
            new_roll, new_pitch, new_yaw = self.k_manager.get_roll_pitch_yaw()

            self.assertAlmostEqual(new_lat, pred_lat, delta=tol_lat_lon)
            self.assertAlmostEqual(new_lon, pred_lon, delta=tol_lat_lon)
            self.assertAlmostEqual(new_alt, initial_alt, delta=tol_alt)

            self.assertAlmostEqual(new_roll,  old_roll,  delta=tol_angle)
            self.assertAlmostEqual(new_pitch, old_pitch, delta=tol_angle)
            self.assertAlmostEqual(new_yaw % 360, old_yaw % 360, delta=tol_angle)