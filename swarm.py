# Student number: 20024094 Daniel Barbu
# Module: Dissertation
# Application title: Visualising swarming behaviour for autonomous drones
# Version: 1.0
# File: swarm.py
# Date: Build across January, February, March, and April
# Date for submission: Deadline 01/05/2026


import random
from drone import Drone
from metrics import Metrics


class Swarm:  # Manages the collection of drone agents and overall swarm behaviour
    def __init__(self, count, width, height, neighbor_dist=60, base_speed=3.0):
        self.width = width
        self.height = height
        self.neighbor_dist = neighbor_dist
        self.base_speed = base_speed
        self.metrics = Metrics()
        self.drones = []
        self.reset(count)

    def reset(self, count):  # Reinitialises the swarm with a new set of drones
        self.drones = [
            Drone(
                random.randint(0, self.width),
                random.randint(0, self.height),
                self.width,
                self.height,
                neighbor_dist=self.neighbor_dist,
                base_speed=self.base_speed
            )
            for _ in range(count)
        ]
        self.metrics.calculate(self.drones)  # Update metrics after reset

    def set_neighbor_distance(self, neighbor_dist):  # Updates sensing distance for all drones
        self.neighbor_dist = neighbor_dist
        for drone in self.drones:
            drone.neighbor_dist = neighbor_dist

    def set_base_speed(self, base_speed):  # Updates base speed for all drones
        self.base_speed = base_speed
        for drone in self.drones:
            drone.base_speed = base_speed

    def update(self, speed_multiplier=1.0):  # Updates behaviour of each drone and recalculates swarm metrics
        for drone in self.drones:
            drone.update(self.drones, speed_multiplier=speed_multiplier)

        self.metrics.calculate(self.drones)

    def draw(self, screen):  # Renders all drones on the simulation screen
        for drone in self.drones:
            drone.draw(screen)