import pygame
from pygame.math import Vector2
from random import uniform

from typing import Self

class Boid:
    def __init__(self, perception: int = 20) -> None:
        window_size_x, window_size_y = pygame.display.get_window_size()
        start_pos = (uniform(0, window_size_x),
                     uniform(0, window_size_y))
        self.position = Vector2(*start_pos)

        self.velocity = Vector2(uniform(-2, 2), uniform(-2, 2))
        self.acceleration = Vector2()
        self.perception = perception

    def align(self, flock: list[Self]):
        local_flock = []
        for boid in flock:
            if self != boid and self.position.distance_to(boid.position) < self.perception:
                local_flock.append(boid)

        # Only align boid if other boids are in it's perception
        if local_flock:
            avg_velocity = Vector2()
            for other_boid in local_flock:
                avg_velocity += other_boid.velocity

            avg_velocity /= len(local_flock)

            interpolated_distance = self.velocity.normalize().lerp(avg_velocity.normalize(), 0.5)

            self.velocity = interpolated_distance * self.velocity.length()

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

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, "white", self.position, 5)

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

