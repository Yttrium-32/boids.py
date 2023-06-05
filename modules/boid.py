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
            logging.error("No value for ICONPATH found in config.")
            sys.exit()
        self.boid_list: list[dict] = list()
            
    def renderable(self):
        for property_dict in self.boid_list:
            boid_rect: pygame.Rect = property_dict["rectangle"]
            boid_rotation = property_dict["rotation"]
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
        self.boid_list.append({ "rectangle": boid_rect, "rotation": boid_rotation, "coords": coords })
        # self.boid_list.append([boid_rect, boid_rotation, coords])

    def update_properties(self, mouse_pos: list[int, int]):
        for i in range(len(self.boid_list)):
            # Changing angle of each boid in boid_list
            # self.boid_list[i]["rotation"] = self.calculate_rotation(mouse_pos, self.boid_list[i]["coords"])
            if self.boid_list[i]["rotation"] >= 360:
                self.boid_list[i]["rotation"] = self.boid_list[i]["rotation"] - 360

    def calculate_rotation(self, mouse_pos: list[int, int], boid_pos: list[int, int]) -> int:
        vector1 = np.array(mouse_pos)
        vector2 = np.array(boid_pos)

        final_vector = np.add(vector2, -vector1)
        x_axis = np.array([1,0])
        dot_product = np.dot(final_vector, x_axis)
        cosine_of_angle = dot_product / np.linalg.norm(final_vector)
        angle_radian = np.arccos(cosine_of_angle)

        return round(180 + np.degrees(angle_radian),2)

