import sys, logging
import pygame
from random import randint

class Boid:
    def __init__(self, settings: dict) -> None:
        try:
            boid_surface = pygame.image.load(settings["ICONPATH"])
            self.boid_surface = pygame.transform.scale(boid_surface, (50,50))
        except KeyError as e:
            logging.error(f"{e}: No value for ICONPATH found in config.")
            sys.exit()
        self.boi_list: list[str] = list()
            
    def renderable(self):
        for boid_rect, boid_rotation in self.boi_list:
            modified_boid_surface = pygame.transform.rotate(self.boid_surface, boid_rotation)
            yield modified_boid_surface, boid_rect

    def generate(self, coords: tuple[int, int]):
        boid_rect = self.boid_surface.get_rect(center = coords)
        boid_rotation = randint(0,360)
        self.boi_list.append((boid_rect, boid_rotation))
