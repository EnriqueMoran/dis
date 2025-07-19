import math
import opendis.RangeCoordinates

from lib.entity.entityManager import EntityManager

from opendis.RangeCoordinates import rad2deg, deg2rad
from opendis.dis7 import Vector3Float, Vector3Double, EulerAngles

__author__ = "EnriqueMoran"

class KinematicsManager:

    def __init__(self) -> None:
        self._gps   = opendis.RangeCoordinates.GPS()
        self._wgs84 = opendis.RangeCoordinates.WGS84()

        lat, lon, alt   = 36.988138186019235, -7.9387833418066025, 0.0
        roll, pitch, yaw  = 0.0, 0.0, 0.0
        self.set_position(lat, lon, alt)
        self.set_orientation(roll, pitch, yaw)
        
    def get_information(self) -> str:
        """TBD
        Note that X, Y, Z can't be 0,0,0.
        """
        gps = opendis.RangeCoordinates.GPS()
        current_lat, current_lon, current_alt = self.get_lat_lon_alt()
        heading = self.get_heading()
        speed   = self.get_speed()
        return  f"current position: {current_lat}, {current_lon}\n" +\
                f"current altitude: {current_alt} m\n" +\
                f"heading: {heading} degrees\n" +\
                f"speed: {speed} m/s"

    def set_orientation(self, roll: float, pitch: float, yaw: float) -> None:
        """
        Set entity orientation in EulerAngles.
        
        :param roll_deg: Roll (bank) in decimal degrees (body-local).
        :param pitch_deg: Pitch (elevation) in decimal degrees (body-local).
        :param yaw_deg: Yaw (heading) in decimal degrees (body-local).
        """
        orientation = EulerAngles()
        orientation.phi   = math.radians(roll)
        orientation.theta = math.radians(pitch)
        orientation.psi   = math.radians(yaw)
        EntityManager().set_entity_orientation(orientation)
    
    def set_position(self, lat: float, lon: float, alt: float) -> None:
        """
        Set entity position (geodetic -> ECEF).
        
        :param lat: Latitude in decimal degrees (geodetic).
        :param lon: Longitude in decimal degrees (geodetic).
        :param alt: Altitude in meters.
        """
        location = Vector3Double()    # Use double precision to preserve altitude accuracy
        location.x, location.y, location.z = self._gps.lla2ecef([lat, lon, alt])
        EntityManager().set_entity_location(location)

    def set_speed(self, speed: float) -> None:
        """"
        Set local NED speed and convert to ECEF.

        :param speed: Speed in meters per second.
        """
        orientation = EntityManager().get_entity_orientation()
        heading_rad = orientation.psi
        pitch_rad   = orientation.theta

        # Compute NED velocity components
        v_n =  speed * math.cos(pitch_rad) * math.cos(heading_rad)
        v_e =  speed * math.cos(pitch_rad) * math.sin(heading_rad)
        v_d = -speed * math.sin(pitch_rad)    # Down positive

        # Convert NED to ECEF
        location = EntityManager().get_entity_location()
        vx, vy, vz = self._gps.ned2ecef([v_n, v_e, v_d], [location.x, location.y, location.z])
        vx = vx - location.x
        vy = vy - location.y
        vz = vz - location.z
        velocity = Vector3Float()
        velocity.x, velocity.y, velocity.z = vx, vy, vz
        EntityManager().set_entity_linear_velocity(velocity)
    
    def set_heading(self, heading: float) -> None:
        """
        Update entity heading (yaw only).

        :param heading: Heading in decimal degrees.
        """
        orientation = EntityManager().get_entity_orientation()
        orientation.psi = math.radians(heading)
        EntityManager().set_entity_orientation(orientation)

    def get_lat_lon_alt(self) -> tuple:
        """Get entity geodetic position from ECEF.

        :return: (lat_deg, lon_deg, alt_m).
        """
        location = EntityManager().get_entity_location()
        return self._gps.ecef2lla([location.x, location.y, location.z])
    
    def get_heading(self) -> float:
        """Get entity heading (yaw).

        :return: Heading in decimal degrees [0,360).
        """
        psi = EntityManager().get_entity_orientation().psi
        deg = math.degrees(psi)
        return deg % 360

    def get_roll_pitch_yaw(self) -> tuple:
        """Get entity roll, pitch, and yaw.

        :return: roll, pitch and yaw in decimal degrees.
        """
        e = EntityManager().get_entity_orientation()
        return (math.degrees(e.phi), math.degrees(e.theta), math.degrees(e.psi))

    def get_speed(self) -> float:
        """Get entity speed in m/s.

        :return: Speed in meters per second.
        """
        speed = EntityManager().get_entity_linear_velocity()
        return math.sqrt(speed.x**2 + speed.y**2 + speed.z**2)

    def process_kinematics(self, dt: float) -> None:
        """
        Update entity position and altitude along kinematics for elapsed time.

        :param dt: Time elapsed since last update in seconds.
        """
        lat, lon, alt = self.get_lat_lon_alt()
        orientation = EntityManager().get_entity_orientation()
        heading = orientation.psi
        pitch   = orientation.theta
        speed   = self.get_speed()

        # Compute horizontal and vertical distances
        horiz_dist = speed * math.cos(pitch) * dt  # ground distance
        vert_dist  = speed * math.sin(pitch) * dt  # altitude change (positive up)

        # Horizontal movement via great-circle arc
        arc = horiz_dist / self._wgs84.a
        lat = math.radians(lat)
        lon = math.radians(lon)

        new_lat_rad = math.asin(math.sin(lat)*math.cos(arc) + 
                                math.cos(lat)*math.sin(arc)*math.cos(heading))
        
        new_lon_rad = lon + math.atan2(math.sin(heading)*math.sin(arc)*math.cos(lat),
                                       math.cos(arc) - math.sin(lat)*math.sin(new_lat_rad))

        # Convert back to geodetic degrees
        new_lat = math.degrees(new_lat_rad)
        new_lon = (math.degrees(new_lon_rad) + 360) % 360
        new_alt = alt + vert_dist

        # Update ECEF position
        x, y, z = self._gps.lla2ecef([new_lat, new_lon, new_alt])
        location = Vector3Double()
        location.x, location.y, location.z = x, y, z
        EntityManager().set_entity_location(location)