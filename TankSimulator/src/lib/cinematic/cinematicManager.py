import math
import opendis.RangeCoordinates

from lib.utils import positionException
from opendis.RangeCoordinates import rad2deg, deg2rad

__author__ = "EnriqueMoran"

class CinematicManager:

    def __init__(self):
        self.initial_pos_x = 0
        self.initial_pos_y = 0
        self.initial_pos_z = 0
        self.pos_x = 0
        self.pos_y = 0
        self.pos_z = 0
        self.speed_x = 0
        self.speed_y = 0
        self.speed_z = 0
        self.psi = 0
        self.theta = 0
        self.phi = 0
    
    def __str__(self):
        return f"initial_pos_x: {self.initial_pos_x}\n" +\
                f"initial_pos_y: {self.initial_pos_y}\n" +\
                f"initial_pos_z: {self.initial_pos_z}\n" +\
                f"pos_x: {self.pos_x}\n" +\
                f"pos_y: {self.pos_y}\n" +\
                f"pos_z: {self.pos_z}\n" +\
                f"speed_x: {self.speed_x}\n" +\
                f"speed_y: {self.speed_y}\n" +\
                f"speed_z: {self.speed_z}\n" +\
                f"psi: {self.psi}\n" +\
                f"theta: {self.theta}\n" +\
                f"phi: {self.phi}"

    def get_information(self):
        """TBD
        Note that X, Y, Z can't be 0,0,0.
        """
        gps = opendis.RangeCoordinates.GPS()
        if self.initial_pos_x == 0 and self.initial_pos_y == 0 and self.initial_pos_z == 0:
            initial_lat = initial_lon = initial_alt = 0
        else:
            initial_lat, initial_lon, initial_alt = gps.ecef2llarpy(self.initial_pos_x,
                                                                    self.initial_pos_y,
                                                                    self.initial_pos_z, 0, 0, 0)[:3]
        current_lat, current_lon, current_alt = self.get_position()
        heading = self.get_heading()
        speed = self.get_speed()
        return f"initial position: {rad2deg(initial_lat)}, {rad2deg(initial_lon)}\n" +\
                f"initial altitude: {initial_alt} m\n" +\
                f"current position: {current_lat}, {current_lon}\n" +\
                f"current altitude: {current_alt} m\n" +\
                f"heading: {heading} degrees\n" +\
                f"speed: {speed} m/s\n"
    
    def set_initial_position(self, lat, lon, alt):
        """
        Set initial position.
        
        :param lat: Latitude in decimal degrees
        :param lon: Longitude in decimal degrees
        :param alt: Altitude in meters
        """
        if lat == 0 and lon == 0 and alt == 0:
            raise positionException.PositionException("Position can't be 0, 0, 0.")

        gps = opendis.RangeCoordinates.GPS()
        pos_x, pos_y, pos_z, psi, theta, phi = gps.llarpy2ecef(deg2rad(lat), deg2rad(lon), alt,
                                                               0, 0, 0)
        self.initial_pos_x = pos_x
        self.initial_pos_y = pos_y
        self.initial_pos_z = pos_z
        self.psi = psi
        self.theta = theta
        self.phi = phi
    
    def set_position(self, lat, lon, alt=None):
        """
        Set current position.
        
        :param lat: Latitude in decimal degrees
        :param lon: Longitude in decimal degrees
        :param alt: Altitude in meters
        """
        alt = self.get_position()[2] if alt is None else alt
        if lat == 0 and lon == 0 and alt == 0:
            raise positionException.PositionException("Position can't be 0, 0, 0.")

        gps = opendis.RangeCoordinates.GPS()
        pos_x, pos_y, pos_z = gps.llarpy2ecef(deg2rad(lat), deg2rad(lon), alt, 0, 0, 0)[:3]
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
    
    def set_speed(self, speed):
        """"
        Set speed.

        :param speed: Speed in meters per second.
        """
        heading_rad = deg2rad(self.get_heading())
        pitch_rad = deg2rad(self.get_roll_pitch_yaw()[1])
        self.speed_x = speed * math.cos(heading_rad) * math.cos(pitch_rad)
        self.speed_y = speed * math.sin(heading_rad) * math.cos(pitch_rad)
        self.speed_z = speed * math.sin(pitch_rad)
    
    def set_heading(self, heading):
        """
        Set heading.

        :param heading: Heading in degrees.
        """
        gps = opendis.RangeCoordinates.GPS()
        lat, lon, alt, roll, pitch, yaw = gps.ecef2llarpy(self.pos_x, self.pos_y, self.pos_z,
                                                          self.psi, self.theta, self.phi)
        yaw = deg2rad(heading)
        psi, theta, phi = gps.llarpy2ecef(lat, lon, alt, roll, pitch, yaw)[3:]
        self.psi = psi
        self.theta = theta
        self.phi = phi
    
    def get_initial_position(self):
        gps = opendis.RangeCoordinates.GPS()
        if self.initial_pos_x == 0 and self.initial_pos_y == 0 and self.initial_pos_z == 0:
            lat = lon = alt = 0
        else:
            lat, lon, alt = gps.ecef2llarpy(self.initial_pos_x, self.initial_pos_y,
                                            self.initial_pos_z, 0, 0, 0)[:3]
        return [rad2deg(lat), rad2deg(lon), alt]

    def get_position(self):
        """Return a vector containing lat, lon and altitude in decimal degrees.
        Note that X, Y, Z can't be 0,0,0."""
        gps = opendis.RangeCoordinates.GPS()
        if self.pos_x == 0 and self.pos_y == 0 and self.pos_z == 0:
            lat = lon = alt = 0
        else:
            lat, lon, alt = gps.ecef2llarpy(self.pos_x, self.pos_y, self.pos_z, self.psi,
                                            self.theta, self.phi)[:3]
        return [rad2deg(lat), rad2deg(lon), alt]
    
    def get_heading(self):
        """Return heading in degrees."""
        gps = opendis.RangeCoordinates.GPS()
        pos_z = self.pos_z
        if self.pos_x == 0 and self.pos_y == 0 and self.pos_z == 0:
            pos_z = 1e-10
        yaw = gps.ecef2llarpy(self.pos_x, self.pos_y, pos_z, self.psi,
                                            self.theta, self.phi)[5]
        heading = rad2deg(yaw)
        heading = heading if heading >= 0 else 360 + heading
        return heading

    def get_roll_pitch_yaw(self):
        """Return a vector containing roll, pitch and yaw in decimal degrees.
        Note that X, Y, Z can't be 0,0,0."""
        gps = opendis.RangeCoordinates.GPS()
        pos_z = self.pos_z
        if self.pos_x == 0 and self.pos_y == 0 and pos_z == 0:
            pos_z = 1e-10
        roll, pitch, yaw = gps.ecef2llarpy(self.pos_x, self.pos_y, pos_z, self.psi, self.theta,
                                           self.phi)[3:]
        return [rad2deg(roll), rad2deg(pitch), rad2deg(yaw)]

    def get_speed(self):
        """Returns speed in m/s."""
        return math.sqrt(self.speed_x**2 + self.speed_y**2 + self.speed_z**2)

    def process_cinematics(self, dt):
        """
        :param dt: Time elapsed since last update in seconds.
        """
        dx = self.speed_x * dt
        dy = self.speed_y * dt
        self.pos_x += dx
        self.pos_y += dy

    def reset_cinematics(self):
        self.pos_x = self.initial_pos_x
        self.pos_y = self.initial_pos_y
        self.pos_z = self.initial_pos_z