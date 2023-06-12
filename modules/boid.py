import sys, logging
import pygame
import numpy as np
from random import randint

class Boid:
    def __init__(self, settings: dict) -> None:
        self.settings = settings
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
        boid_rotation = randint(0,360)
        boid_rect = self.boid_surface.get_rect(center = coords)
        self.boid_list.append({ "rectangle": boid_rect, "rotation": boid_rotation, "coords": coords })

        # self.boid_list.append([boid_rect, boid_rotation, coords])
    def update_properties(self, mouse_pos: list[int, int]):
        for i in range(len(self.boid_list)):
            # Changing angle of each boid in boid_list
            self.boid_list[i]["rotation"] = self.calculate_rotation(mouse_pos, self.boid_list[i]["rectangle"].center)
            if self.boid_list[i]["rotation"] >= 360:
                self.boid_list[i]["rotation"] = self.boid_list[i]["rotation"] - 360

            current_rect = self.boid_list[i]["rectangle"]

            self.boid_list[i]["rectangle"] = self.calculate_new_rect(current_rect, self.boid_list[i]["rotation"])
    def calculate_rotation(self, mouse_pos: list[int, int], boid_pos: list[int, int]) -> int:
        mouse_vector = np.array(mouse_pos) # Vector of mouse coords
        boid_vector = np.array(boid_pos) # Vector of boid coords

        final_vector = np.add(boid_vector, -mouse_vector)
        x_axis = np.array([1,0])
        dot_product = np.dot(final_vector, x_axis)
        cosine_of_angle = dot_product / np.linalg.norm(final_vector)
        angle_radian = np.arccos(cosine_of_angle)

        final_rotation = 180 + round(np.degrees(angle_radian),2)

        if mouse_vector[1] < boid_vector[1]:
            return 360 - final_rotation
        else:
            return final_rotation

    def calculate_new_rect(self, current_rect: pygame.Rect, angle: int):
        new_rect: pygame.Rect = current_rect
        # new_rect.x += self.calculate_distance()
        new_rect.x += 10
        new_rect.y += 10

        # Screen wrap implementation
        # The -10 and +30 is to ensure the rectangle is loaded and unloaded off screen
        # Since the rectangle doesn't perfectly align with the sprite
        if new_rect.x >= self.settings["WIDTH"] - 10:
            new_rect.x -= self.settings["WIDTH"] + 30
        if new_rect.y >= self.settings["HEIGHT"] - 10:
            new_rect.y -= self.settings["HEIGHT"] + 30

        return new_rect

    def calculate_distance(self, x_coord: int, y_coord: int, angle: int):
        next_x_coord = self.settings["WIDTH"]
        next_y_coord = np.tan(angle) * (next_x_coord - x_coord) + y_coord

