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

    def __init__(self, left_bottom_corner, right_top_corner):
        self.lb_corner = left_bottom_corner
        self.rt_corner = right_top_corner

    @classmethod
    def initialize_zones(cls):
        for latitude in range(cls.MIN_LATITUDE, cls.MAX_LATITUDE, cls.DEGREE_HEIGHT):
            for longitude in range(cls.MIN_LONGITUDE, cls.MAX_LONGITUDE, cls.DEGREE_WIDTH):
                zone = Zone(Position(latitude, longitude),
                            Position(latitude + 1, longitude + 1))
                cls.ZONES.append(zone)


def main():
    with open("agents-100k.json", "r") as agents:
        agents = json.load(agents)
        for agent_attributes in agents:
            latitude = agent_attributes.pop("latitude")
            longitude = agent_attributes.pop("longitude")
            position = Position(latitude, longitude)
            agent = Agent(position, **agent_attributes)
            Zone.initialize_zones()


if __name__ == "__main__":
    main()
