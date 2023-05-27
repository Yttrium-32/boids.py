import sys, logging
import pygame

class Boid:
    def __init__(self, settings: dict) -> None:
        try:
            boid_surface = pygame.image.load(settings["ICONPATH"])
            self.boid_surface = pygame.transform.scale(boid_surface, (50,50))
        except KeyError as e:
            logging.error(f"{e}: No value for ICONPATH found in config.")
            sys.exit()
            
    def renderable(self, postions: list[tuple[int, int]]):
        for coords in postions:
            boid_rect = self.boid_surface.get_rect(center = coords)
            yield self.boid_surface, boid_rect
