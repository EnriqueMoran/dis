import math
import opendis.RangeCoordinates

from lib.entity import entityManager

from opendis.RangeCoordinates import rad2deg, deg2rad
from opendis.dis7 import Vector3Float, Vector3Double, EulerAngles

__author__ = "EnriqueMoran"

class KinematicsManager:

    def __init__(self):
        orientation = EulerAngles()    # Set valid 0, 0, 0 orientation
        orientation.psi   = -3.141592653489793
        orientation.theta = -1.5707963266948965
        orientation.phi   = 3.141592653589793
        entityManager.EntityManager().set_entity_orientation(orientation)

    def get_information(self):
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
        location.x, location.y, location.z = gps.lla2ecef([lat, lon, alt])
        entityManager.EntityManager().set_entity_location(location)

    def set_speed(self, speed):
        """"
        Set speed.

        :param speed: Speed in meters per second.
        """
        heading_rad = deg2rad(self.get_heading())
        pitch_rad   = deg2rad(self.get_roll_pitch_yaw()[1])
        velocity   = Vector3Float()
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

        location    = entityManager.EntityManager().get_entity_location()
        orientation = entityManager.EntityManager().get_entity_orientation()
        lat, lon, alt, roll, pitch, _ = gps.ecef2llarpy(location.x, location.y, location.z,
                                                        orientation.psi, orientation.theta,
                                                        orientation.phi)
        yaw = deg2rad(heading)
        orientation.psi, orientation.theta, orientation.phi = gps.llarpy2ecef(lat, lon, alt,
                                                                              roll, pitch, yaw)[3:]
        entityManager.EntityManager().set_entity_orientation(orientation)

    def get_lat_lon_alt(self):
        """Return a vector containing lat, lon and altitude in decimal degrees and meters.
        Note that X, Y, Z can't be 0,0,0."""
        gps = opendis.RangeCoordinates.GPS()
        location = entityManager.EntityManager().get_entity_location()
        return gps.ecef2lla([location.x, location.y, location.z])
    
    def get_heading(self):
        """Return heading in degrees."""
        gps = opendis.RangeCoordinates.GPS()
        location    = entityManager.EntityManager().get_entity_location()
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
        location    = entityManager.EntityManager().get_entity_location()
        orientation = entityManager.EntityManager().get_entity_orientation()
        roll, pitch, yaw = gps.ecef2llarpy(location.x, location.y, location.z,
                                           orientation.psi, orientation.theta, orientation.phi)[3:]
        return [rad2deg(roll), rad2deg(pitch), rad2deg(yaw)]

    def get_speed(self):
        """Returns speed in m/s."""
        speed = entityManager.EntityManager().get_entity_linear_velocity()
        return math.sqrt(speed.x**2 + speed.y**2 + speed.z**2)

    def process_kinematics(self, dt):
        """
        :param dt: Time elapsed since last update in seconds.
        Does not calculate new Altitude.

        Return traveled distance in meters.
        """
        lat_d, lon_d, alt = self.get_lat_lon_alt()
        current_lat = deg2rad(lat_d)
        current_lon = deg2rad(lon_d)
        heading = deg2rad(self.get_heading())
        speed   = self.get_speed()

        distance = (speed * dt) / (opendis.RangeCoordinates.WGS84().a)
        new_lat = math.asin(math.sin(current_lat) * math.cos(distance) + math.cos(current_lat) * \
                            math.sin(distance) * math.cos(heading))
        new_lon = current_lon + math.atan2(math.sin(heading) * math.sin(distance) * \
                                           math.cos(current_lat), math.cos(distance) - \
                                           math.sin(current_lat) * math.sin(new_lat))

        gps = opendis.RangeCoordinates.GPS()
        location = Vector3Double() 
        location.x, location.y, location.z = gps.lla2ecef([rad2deg(new_lat), rad2deg(new_lon), alt])
        entityManager.EntityManager().set_entity_location(location)

        return (speed * dt)