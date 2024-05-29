import pygame
from pygame.math import Vector2

class Boid:
    def __init__(self) -> None:
        self.position = Vector2
        self.velocity = Vector2
        self.acceleration = Vector2

    def draw(self, screen: pygame.Surface, coord: tuple[int, int] = (0, 0)):
        pygame.draw.rect(screen, "white", (*coord, 50, 50))
