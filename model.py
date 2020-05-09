#! /usr/bin/env python
# coding: utf-8
import json
import math


class Agent:

    def __init__(self, position, **agent_attributes):
        self.position = position
        for attr_name, attr_value in agent_attributes.items():
            setattr(self, attr_name, attr_value)


class Position:

    def __init__(self, latitude_degrees, longitude_degrees):
        self.latitude_degrees = latitude_degrees
        self.longitude_degrees = longitude_degrees

    @property
    def latitude(self):
        return self.latitude_degrees * math.pi / 180

    @property
    def longitude(self):
        return self.longitude_degrees * math.pi / 180


class Zone:

    ZONES = []
    MIN_LONGITUDE = -180
    MAX_LONGITUDE = 180
    MIN_LATITUDE = -90
    MAX_LATITUDE = 90
    DEGREE_WIDTH = 1
    DEGREE_HEIGHT = 1
    EARTH_RADIUS_KILOMETERS = 6371

    def __init__(self, left_bottom_corner, right_top_corner):
        self.lb_corner = left_bottom_corner
        self.rt_corner = right_top_corner
        self.inhabitants = []

    def add_inhabitant(self, inhabitant):
        self.inhabitants.append(inhabitant)

    @property
    def population(self):
        return len(self.inhabitants)

    @property
    def width(self):
        return abs((self.lb_corner.longitude - self.rt_corner.longitude) * self.EARTH_RADIUS_KILOMETERS)

    @property
    def height(self):
        return abs((self.lb_corner.latitude - self.rt_corner.latitude) * self.EARTH_RADIUS_KILOMETERS)

    @property
    def area(self):
        return self.height * self.width

    @property
    def density(self):
        return self.population / self.area

    def avg_agreeableness(self):
        return 0 if not self.population else sum(inhabitant.agreeableness / self.population for inhabitant in self.inhabitants)

    @classmethod
    def _initialize_zones(cls):
        for latitude in range(cls.MIN_LATITUDE, cls.MAX_LATITUDE, cls.DEGREE_HEIGHT):
            for longitude in range(cls.MIN_LONGITUDE, cls.MAX_LONGITUDE, cls.DEGREE_WIDTH):
                zone = Zone(Position(latitude, longitude),
                            Position(latitude + 1, longitude + 1))
                cls.ZONES.append(zone)

    @classmethod
    def find_zone_of_position(cls, position):
        if not cls.ZONES:
            cls._initialize_zones()
        #The zone is made of 64800 zones, (from 0 to 64799), wich can be divided in 180 rows and 360 columns.
        # Longitude index:
        # position.longitude_degree = -50 >> 130
        longitude_index = int(
            (position.longitude_degrees - cls.MIN_LONGITUDE) / cls.DEGREE_WIDTH)
        # Number of columns per row:
        longitude_degrees = int(
            (cls.MAX_LONGITUDE - cls.MIN_LONGITUDE) / cls.DEGREE_WIDTH)  # 360
        # Latitude row:
        # position.latitude_degree = 5 >> 95
        latitude_row = int((position.latitude_degrees -
                            cls.MIN_LATITUDE) / cls.DEGREE_HEIGHT)
        # There is {longitude_degrees} (360) index between two {latitude_row}.
        # Laitude index:
        # position.latitude_degree = 5 >> 95 * 360 = 34 200
        latitude_index = latitude_row * longitude_degrees
        # position(5, -50) >> 34200 + 130 = 34330
        index_zone = latitude_index + longitude_index
        assert (index_zone < 64800 and index_zone > -1)
        return cls.ZONES[index_zone]


def main():
    with open("agents-100k.json", "r") as agents:
        agents = json.load(agents)
        for agent_attributes in agents:
            latitude = agent_attributes.pop("latitude")
            longitude = agent_attributes.pop("longitude")
            position = Position(latitude, longitude)
            agent = Agent(position, **agent_attributes)
            zone = Zone.find_zone_of_position(position)
            zone.add_inhabitant(agent)
            print(zone.avg_agreeableness())


if __name__ == "__main__":
    main()
