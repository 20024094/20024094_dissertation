# Student number: 20024094 Daniel Barbu
# Module: Dissertation
# Application title: Visualising swarming behaviour for autonomous drones
# Version: 1.0
# File: drone.py
# Date: Build across January, February, March, and April
# Date for submission: Deadline 01/05/2026

import math
import random
import pygame


class Drone:  # Represents an individual autonomous agent within the swarm
    def __init__(self, x, y, width, height, neighbor_dist=60, base_speed=3.0):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height

        self.neighbor_dist = neighbor_dist  # Local sensing distance
        self.base_speed = base_speed        # Base movement speed

        angle = random.uniform(0, 2 * math.pi)  # Initialise random movement direction and velocity
        speed = random.uniform(1.5, 3.0)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.max_speed = base_speed
        self.max_force = 0.08

    def distance_to(self, other):  # Calculates distance to another drone
        return math.hypot(self.x - other.x, self.y - other.y)

    def limit_vector(self, x, y, max_value):  # Limits magnitude of a vector to maintain stability
        magnitude = math.hypot(x, y)
        if magnitude > max_value and magnitude > 0:
            x = (x / magnitude) * max_value
            y = (y / magnitude) * max_value
        return x, y

    def separation(self, drones, desired_separation=25):  # Implements separation rule (collision avoidance)
        steer_x = 0.0
        steer_y = 0.0
        count = 0

        for other in drones:
            if other is self:
                continue

            d = self.distance_to(other)
            if 0 < d < desired_separation:
                diff_x = self.x - other.x
                diff_y = self.y - other.y

                if d > 0:
                    diff_x /= d
                    diff_y /= d

                steer_x += diff_x
                steer_y += diff_y
                count += 1

        if count > 0:
            steer_x /= count
            steer_y /= count

        if steer_x != 0 or steer_y != 0:
            steer_x, steer_y = self.limit_vector(steer_x, steer_y, self.max_speed)
            steer_x -= self.vx
            steer_y -= self.vy
            steer_x, steer_y = self.limit_vector(steer_x, steer_y, self.max_force)

        return steer_x, steer_y

    def alignment(self, drones):  # Implements alignment rule (velocity matching with neighbours)
        avg_vx = 0.0
        avg_vy = 0.0
        count = 0

        for other in drones:
            if other is self:
                continue

            d = self.distance_to(other)
            if d < self.neighbor_dist:
                avg_vx += other.vx
                avg_vy += other.vy
                count += 1

        if count > 0:
            avg_vx /= count
            avg_vy /= count

            avg_vx, avg_vy = self.limit_vector(avg_vx, avg_vy, self.max_speed)
            steer_x = avg_vx - self.vx
            steer_y = avg_vy - self.vy
            steer_x, steer_y = self.limit_vector(steer_x, steer_y, self.max_force)
            return steer_x, steer_y

        return 0.0, 0.0

    def cohesion(self, drones):  # Implements cohesion rule (move towards group center)
        center_x = 0.0
        center_y = 0.0
        count = 0

        for other in drones:
            if other is self:
                continue

            d = self.distance_to(other)
            if d < self.neighbor_dist:
                center_x += other.x
                center_y += other.y
                count += 1

        if count > 0:
            center_x /= count
            center_y /= count
            return self.seek(center_x, center_y)

        return 0.0, 0.0

    def seek(self, target_x, target_y):  # Steering behaviour towards a target position
        desired_x = target_x - self.x
        desired_y = target_y - self.y

        desired_x, desired_y = self.limit_vector(desired_x, desired_y, self.max_speed)

        steer_x = desired_x - self.vx
        steer_y = desired_y - self.vy
        steer_x, steer_y = self.limit_vector(steer_x, steer_y, self.max_force)

        return steer_x, steer_y

    def update(self, drones, speed_multiplier=1.0):  # Updates drone behaviour by combining swarm rules
        self.max_speed = self.base_speed * speed_multiplier

        sep_x, sep_y = self.separation(drones)
        ali_x, ali_y = self.alignment(drones)
        coh_x, coh_y = self.cohesion(drones)

        separation_weight = 1.5
        alignment_weight = 1.0
        cohesion_weight = 1.0

        self.vx += sep_x * separation_weight + ali_x * alignment_weight + coh_x * cohesion_weight
        self.vy += sep_y * separation_weight + ali_y * alignment_weight + coh_y * cohesion_weight

        self.vx, self.vy = self.limit_vector(self.vx, self.vy, self.max_speed)

        self.x += self.vx
        self.y += self.vy

        self.wrap_edges()  # Handle boundary behaviour

    def wrap_edges(self):  # Wraps drones around simulation boundaries (toroidal space)
        if self.x < 0:
            self.x = self.width
        elif self.x > self.width:
            self.x = 0

        if self.y < 0:
            self.y = self.height
        elif self.y > self.height:
            self.y = 0

    def draw(self, screen):  # Renders drone as directional triangle
        angle = math.atan2(self.vy, self.vx)

        size = 8
        front = (
            self.x + math.cos(angle) * size,
            self.y + math.sin(angle) * size
        )
        left = (
            self.x + math.cos(angle + 2.5) * size,
            self.y + math.sin(angle + 2.5) * size
        )
        right = (
            self.x + math.cos(angle - 2.5) * size,
            self.y + math.sin(angle - 2.5) * size
        )

        pygame.draw.polygon(screen, (0, 200, 255), [front, left, right])