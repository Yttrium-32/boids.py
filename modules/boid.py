import pygame
from pygame.math import Vector2
from random import uniform, choice

from typing import Self

class Boid:
    def __init__(self, perception: int = 30) -> None:
        window_size_x, window_size_y = pygame.display.get_window_size()
        start_pos = (uniform(0, window_size_x),
                     uniform(0, window_size_y))
        self.position = Vector2(*start_pos)

        self.velocity = Vector2(choice([-3, 3]), choice([-3, 3]))
        self.acceleration = Vector2()
        self.perception = perception

        self.steering_force = 0.5
        self.steering_vectors = []

    def get_avg_velocity(self, flock: list[Self]):
        local_flock = []
        for boid in flock:
            behind_boid = self.velocity.angle_to(boid.velocity) < 30 \
                          or self.velocity.angle_to(boid.velocity) > 330
            perceived = self != boid \
                        and self.position.distance_to(boid.position) < self.perception \
                        and behind_boid
            if perceived:
                local_flock.append(boid)

        # Only calc avg_velocity if other boids are in perception radius
        avg_velocity = Vector2()
        if local_flock:
            for other_boid in local_flock:
                avg_velocity += other_boid.velocity

            avg_velocity /= len(local_flock)

        return avg_velocity

    def align(self, avg_velocity: Vector2):
        if avg_velocity.magnitude() != 0:
            self.steering_vectors.append(avg_velocity.normalize())

    def cohesion(self, avg_velocity: Vector2):
        if avg_velocity.magnitude() != 0:
            avg_velocity -= self.position
            self.steering_vectors.append(avg_velocity.normalize())

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

        avg_velocity = self.get_avg_velocity(flock)

        # The three rules
        self.align(avg_velocity)
        self.cohesion(avg_velocity)

        # Only steer boid if steering vectors exist
        if self.steering_vectors:
            average_steering_vector = Vector2()
            for vec in self.steering_vectors:
                average_steering_vector += vec
            average_steering_vector /= len(self.steering_vectors)

            interpolated_distance = self.velocity.normalize()\
                    .lerp(average_steering_vector.normalize(), self.steering_force)
            self.velocity = interpolated_distance * self.velocity.length()

        self.wrap()

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, "white", self.position, 5)

