# Student number: 20024094 Daniel Barbu
# Module: Dissertation
# Application title: Visualising swarming behaviour for autonomous drones
# Version: 1.0
# File: metrics.py
# Date: Build across January, February, March, and April
# Date for submission: Deadline 01/05/2026

import math


class Metrics:  # Handles performance measurement of the swarm system
    def __init__(self):
        self.collisions = 0
        self.total_distance = 0.0
        self.distance_count = 0

    def reset(self):  # Resets all metrics before a new calculation cycle
        self.collisions = 0
        self.total_distance = 0.0
        self.distance_count = 0

    def calculate(self, drones):  # Computes pairwise distances and detects collisions between drones
        self.reset()

        for i in range(len(drones)):
            for j in range(i + 1, len(drones)):
                d = math.hypot(
                    drones[i].x - drones[j].x,
                    drones[i].y - drones[j].y
                )

                if d < 10:  # Checks if drones are within collision threshold
                    self.collisions += 1

                self.total_distance += d  # Accumulates distance for average calculation
                self.distance_count += 1

    def average_distance(self):  # Returns the average distance between all drones
        if self.distance_count == 0:
            return 0.0
        return self.total_distance / self.distance_count