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

        self.velocity = Vector2(uniform(-0.5, 0.5), uniform(-0.5, 0.5))
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

            try:
                avg_velocity /= len(local_flock)
            except ZeroDivisionError:
                # If the only boid in the local_flock is self, don't update avg_velocity
                ...

            steering_force = avg_velocity - self.velocity
            self.acceleration = steering_force # Since mass of all boids is 1

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, "white", self.position, 5)

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration

