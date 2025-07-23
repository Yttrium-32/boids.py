import pygame
from pygame.math import Vector2

from random import uniform
from typing import Self


class Boid:
    non_perceived_angle = 60
    perception = 50
    max_vec_val = 3

    def __init__(self) -> None:
        window_size_x, window_size_y = pygame.display.get_window_size()
        start_pos = (uniform(0, window_size_x), uniform(0, window_size_y))

        self.position = Vector2(*start_pos)

        self.velocity = Vector2(
            uniform(0, Boid.max_vec_val), uniform(0, Boid.max_vec_val)
        )
        self.acceleration = Vector2()

        self.steering_vectors: list[Vector2] = []

    def find_local_flock(self, flock: list[Self]):
        local_flock = []
        for other_boid in flock:
            behind_boid = (
                self.velocity.angle_to(other_boid.velocity) < Boid.non_perceived_angle
                or self.velocity.angle_to(other_boid.velocity)
                > 360 - Boid.non_perceived_angle
            )
            perceived = (
                self != other_boid
                and self.position.distance_to(other_boid.position) < Boid.perception
                and behind_boid
            )
            if perceived:
                local_flock.append(other_boid)

        return local_flock

    def get_avg_velocity(self, local_flock: list[Self]):
        avg_velocity = Vector2()

        # Only calc avg_velocity if other boids are in perception radius
        if local_flock:
            for other_boid in local_flock:
                avg_velocity += other_boid.velocity

            avg_velocity /= len(local_flock)

        return avg_velocity

    def get_avg_postion(self, local_flock: list[Self]):
        avg_position = Vector2()

        # Only calc avg_position if other boids are in perception radius
        if local_flock:
            for other_boid in local_flock:
                avg_position += other_boid.position

            avg_position /= len(local_flock)

        return avg_position

    def align(self, avg_velocity: Vector2):
        if avg_velocity.magnitude() != 0:
            steering_vec = avg_velocity - self.velocity
            self.steering_vectors.append(steering_vec)

    def cohesion(self, avg_position: Vector2):
        if avg_position.magnitude() != 0:
            steering_vec = avg_position - self.position

            # Cohesion tends to overwhelm other forces without this
            steering_vec.clamp_magnitude_ip(Boid.max_vec_val)
            self.steering_vectors.append(steering_vec)

    def separation(self, local_flock: list[Self]):
        # Only separate if a local flock exists
        if not local_flock:
            return

        for other_boid in local_flock:
            distance = self.position.distance_to(other_boid.position)
            diff_vec = self.position - other_boid.position

            # Higher distance results in a smaller separation vector
            # i.e. separation vector is inversely proportional to distance
            seperation_vec = diff_vec / distance
            self.steering_vectors.append(seperation_vec)

    def wrap(self):
        window_size_x, window_size_y = pygame.display.get_window_size()
        if self.position.x > window_size_x:
            self.position.x -= window_size_x
        elif self.position.x < 0:
            self.position.x += window_size_x

        if self.position.y > window_size_y:
            self.position.y -= window_size_y
        elif self.position.y < 0:
            self.position.y += window_size_y

    def update(self, flock: list[Self]):
        self.position += self.velocity
        self.velocity += self.acceleration

        # Stop boids from moving too fast
        self.velocity.clamp_magnitude_ip(Boid.max_vec_val)

        local_flock = self.find_local_flock(flock)
        avg_velocity = self.get_avg_velocity(local_flock)
        avg_position = self.get_avg_postion(local_flock)

        # The three rules
        self.align(avg_velocity)
        self.cohesion(avg_position)
        self.separation(local_flock)

        # Only steer boid if steering vectors is not empty
        if self.steering_vectors:
            average_steering_vector = Vector2()
            for vec in self.steering_vectors:
                average_steering_vector += vec
            average_steering_vector /= len(self.steering_vectors)

            self.acceleration = average_steering_vector

            # Remove all steering vectors that have been applied
            self.steering_vectors.clear()

        self.wrap()

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, "white", self.position, 5)
