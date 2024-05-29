import pygame
from pygame.math import Vector2
from random import randint

class Boid:
    def __init__(self) -> None:
        window_size_x, window_size_y = pygame.display.get_window_size()
        self.position = Vector2(window_size_x / 2, window_size_y / 2)

        self.velocity = Vector2(randint(-10, 10), randint(-10, 10))
        self.acceleration = Vector2()

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, "white", (*self.position, 50, 50))

    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
