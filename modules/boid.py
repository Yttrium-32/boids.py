import sys, logging
import pygame
import numpy as np
from random import randint

class Boid:
    def __init__(self, settings: dict) -> None:
        try:
            boid_surface = pygame.image.load(settings["ICONPATH"])
            self.boid_surface = pygame.transform.scale(boid_surface, (50,50))
        except KeyError as e:
            logging.error(f"{e}: No value for ICONPATH found in config.")
            sys.exit()
        self.boid_list: list[list] = list()
            
    def renderable(self):
        for property_list in self.boid_list:
            boid_rect: pygame.Rect = property_list[0]
            boid_rotation = property_list[1]
            try:
                modified_boid_surface = pygame.transform.rotate(self.boid_surface, boid_rotation)
            except pygame.error: 
                modified_boid_surface = self.boid_surface
            boid_properties = {
                "surface": modified_boid_surface, 
                "rectangle": boid_rect, 
                "rotation": boid_rotation
            }

            yield boid_properties

    def generate(self, coords: tuple[int, int]):
        boid_rect = self.boid_surface.get_rect(center = coords)
        boid_rotation = randint(0,360)
        self.boid_list.append([boid_rect, boid_rotation, coords])

    def update_properties(self, mouse_x: int):
        for i in range(len(self.boid_list)):
            # Changing angle of each boid in boid_list
            self.boid_list[i][1] = self.calculate_rotation(self.boid_list[i][2], mouse_x)
            if self.boid_list[i][1] >= 360:
                self.boid_list[i][1] = self.boid_list[i][1] - 360

    def calculate_rotation(self, boid_coords: tuple[int,int], mouse_x: int) -> int:
        rotation: int = 0

        x_vector = np.array([mouse_x,0])
        boid_vector = np.array(boid_coords)

        dot_product = np.dot(x_vector, boid_vector)
        scalar_prodcut = np.linalg.norm(x_vector) * np.linalg.norm(boid_vector)

        angle_radian = np.arccos(dot_product / scalar_prodcut)
        rotation = np.degrees(angle_radian)

        print(f"{boid_vector=}")
        return rotation
