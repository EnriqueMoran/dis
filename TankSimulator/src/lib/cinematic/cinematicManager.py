import math
import opendis.RangeCoordinates

from lib.entity import entityManager

from lib.utils import positionException
from opendis.RangeCoordinates import rad2deg, deg2rad
from opendis.dis7 import Vector3Float, Vector3Double, EulerAngles

__author__ = "EnriqueMoran"

class CinematicManager:

    def __init__(self):
        orientation = EulerAngles()    # Set valid 0, 0, 0 orientation
        orientation.psi = -3.141592653489793
        orientation.theta = -1.5707963266948965
        orientation.phi = 3.141592653589793
        entityManager.EntityManager().set_entity_orientation(orientation)

    def get_information(self):
        """TBD
        Note that X, Y, Z can't be 0,0,0.
        """
        gps = opendis.RangeCoordinates.GPS()
        current_lat, current_lon, current_alt = self.get_lat_lon_alt()
        heading = self.get_heading()
        speed = self.get_speed()
        return  f"current position: {current_lat}, {current_lon}\n" +\
                f"current altitude: {current_alt} m\n" +\
                f"heading: {heading} degrees\n" +\
                f"speed: {speed} m/s\n"
    
    def set_position(self, lat, lon, alt=None):
        """
        Set current position.
        
        :param lat: Latitude in decimal degrees
        :param lon: Longitude in decimal degrees
        :param alt: Altitude in meters
        """
        alt = self.get_lat_lon_alt()[2] if alt is None else alt

        gps = opendis.RangeCoordinates.GPS()
        location = Vector3Float() 
        location.x, location.y, location.z = gps.lla2ecef([deg2rad(lat), deg2rad(lon), alt])
        entityManager.EntityManager().set_entity_location(location)

    def set_speed(self, speed):
        """"
        Set speed.

        :param speed: Speed in meters per second.
        """
        heading_rad = deg2rad(self.get_heading())
        pitch_rad = deg2rad(self.get_roll_pitch_yaw()[1])
        velocity = Vector3Float()
        velocity.x = speed * math.cos(heading_rad) * math.cos(pitch_rad)
        velocity.y = speed * math.sin(heading_rad) * math.cos(pitch_rad)
        velocity.z = speed * math.sin(pitch_rad)
        entityManager.EntityManager().set_entity_linear_velocity(velocity)
    
    def set_heading(self, heading):
        """
        Set heading.

        :param heading: Heading in degrees.
        """
        gps = opendis.RangeCoordinates.GPS()

        location = entityManager.EntityManager().get_entity_location()
        orientation = entityManager.EntityManager().get_entity_orientation()
        lat, lon, alt, roll, pitch, _ = gps.ecef2llarpy(location.x, location.y, location.z,
                                                        orientation.psi, orientation.theta,
                                                        orientation.phi)
        yaw = deg2rad(heading)
        orientation.psi, orientation.theta, orientation.phi = gps.llarpy2ecef(lat, lon, alt,
                                                                              roll, pitch, yaw)[3:]
        entityManager.EntityManager().set_entity_orientation(orientation)

    def get_lat_lon_alt(self):
        """Return a vector containing lat, lon and altitude in decimal degrees.
        Note that X, Y, Z can't be 0,0,0."""
        gps = opendis.RangeCoordinates.GPS()
        location = entityManager.EntityManager().get_entity_location()
        return gps.ecef2lla([location.x, location.y, location.z])
    
    def get_heading(self):
        """Return heading in degrees."""
        gps = opendis.RangeCoordinates.GPS()
        location = entityManager.EntityManager().get_entity_location()
        orientation = entityManager.EntityManager().get_entity_orientation()
        yaw = gps.ecef2llarpy(location.x, location.y, location.z,
                              orientation.psi, orientation.theta, orientation.phi)[5]
        heading = rad2deg(yaw)
        heading = heading if heading >= 0 else 360 + heading
        return heading

    def get_roll_pitch_yaw(self):
        """Return a vector containing roll, pitch and yaw in decimal degrees.
        Note that X, Y, Z can't be 0,0,0."""
        gps = opendis.RangeCoordinates.GPS()
        location = entityManager.EntityManager().get_entity_location()
        orientation = entityManager.EntityManager().get_entity_orientation()
        roll, pitch, yaw = gps.ecef2llarpy(location.x, location.y, location.z,
                                           orientation.psi, orientation.theta, orientation.phi)[3:]
        return [rad2deg(roll), rad2deg(pitch), rad2deg(yaw)]

    def get_speed(self):
        """Returns speed in m/s."""
        speed = entityManager.EntityManager().get_entity_linear_velocity()
        return math.sqrt(speed.x**2 + speed.y**2 + speed.z**2)

    def process_cinematics(self, dt):
        """
        :param dt: Time elapsed since last update in seconds.

        Return traveled distance in meters.
        """
        current_location = location = entityManager.EntityManager().get_entity_location()
        new_location = Vector3Double()
        speed = entityManager.EntityManager().get_entity_linear_velocity()
        dx = speed.x * dt
        dy = speed.y * dt
        new_location.x = current_location.x + dx
        new_location.y = current_location.y + dy
        new_location.z = current_location.z
        entityManager.EntityManager().set_entity_location(new_location)
        return math.sqrt(dx**2 + dy**2)