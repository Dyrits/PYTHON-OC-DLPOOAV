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


def main():
    with open("agents-100k.json", "r") as agents:
        agents = json.load(agents)
        for agent_attributes in agents:
            latitude = agent_attributes.pop("latitude")
            longitude = agent_attributes.pop("longitude")
            position = Position(latitude, longitude)
            agent = Agent(position, **agent_attributes)


if __name__ == "__main__":
    main()
