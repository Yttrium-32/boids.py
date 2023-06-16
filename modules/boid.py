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
        except KeyError:
            logging.error("No value for ICONPATH found in config.")
            sys.exit()
        self.boid_list: list[dict] = list()
        self.wrap = 0
            
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
        boid_rotation = randint(0, 360)
        boid_rect = self.boid_surface.get_rect(center = coords)
        self.boid_list.append({ "rectangle": boid_rect, "rotation": boid_rotation, "coords": coords })

    def update_properties(self, mouse_pos: list[int, int]):
        for i in range(len(self.boid_list)):
            # Changing angle of each boid in boid_list
            try:
                if self.settings["FOLLOW_MOUSE"]:
                    angle = self.calculate_rotation(mouse_pos, self.boid_list[i]["rectangle"].center)
                else: 
                    angle = self.boid_list[i]["rotation"]
            except Exception as e:
                logging.error(f"{e}: No value for FOLLOW_MOUSE found in config.")
                sys.exit()

            self.boid_list[i]["rotation"] = angle
            if self.boid_list[i]["rotation"] >= 360:
                self.boid_list[i]["rotation"] = self.boid_list[i]["rotation"] - 360

            current_rect = self.boid_list[i]["rectangle"]

            self.boid_list[i]["rectangle"] = self.calculate_new_rect(current_rect, angle)

    def calculate_new_rect(self, current_rect: pygame.Rect, angle: int):
        new_rect: pygame.Rect = current_rect
        center_coords = current_rect.center
        try:
            new_coords = self.calculate_distance(self.settings["SPEED"], center_coords, angle)
        except KeyError:
            logging.error("Value for SPEED not defined in config.")
            sys.exit()
        new_rect.center: tuple[int, int] = new_coords

        # Screen wrap implementation
        # The -10 and +30 is to ensure the rectangle is loaded and unloaded off screen
        # Since the rectangle doesn't perfectly align with the sprite
        if not self.wrap:
            # Screen wrap vertically
            if new_rect.x >= self.settings["WIDTH"] :
                new_rect.x -= self.settings["WIDTH"]
                self.wrap = 1
            if new_rect.x <= 0:
                new_rect.x = self.settings["WIDTH"]
                self.wrap = 1

            # Screen wrap horizontally
            if new_rect.y >= self.settings["HEIGHT"]:
                new_rect.y -= self.settings["HEIGHT"]
                self.wrap = 1
            if new_rect.y <= 0:
                new_rect.y = self.settings["HEIGHT"]
                self.wrap = 1
        else:
            self.wrap = 0

        return new_rect

    def calculate_rotation(self, mouse_pos: list[int, int], boid_pos: list[int, int]) -> int:
        mouse_vector = np.array(mouse_pos) # Vector of mouse coords
        boid_vector = np.array(boid_pos) # Vector of boid coords

        # if the position of the mouse and boid coincide the sprite does not render
        # This doesn't really ever happen except for a split second when the boid is created
        # To prevent this from happening we simply don't calculate a new vector
        if boid_vector[0] != mouse_vector[0] or boid_vector[1] != mouse_vector[1] :
            final_vector = np.add(boid_vector, -mouse_vector)
        else:
            final_vector = boid_vector

        x_axis = np.array([1,0])
        dot_product = np.dot(final_vector, x_axis)
        cosine_of_angle = dot_product / np.linalg.norm(final_vector)
        angle_radian = np.arccos(cosine_of_angle)

        final_rotation = 180 + round(np.degrees(angle_radian),2)

        if mouse_vector[1] < boid_vector[1]:
            return 360 - final_rotation
        else:
            return final_rotation

    def update_settings(self, new_settings):
        self.settings = new_settings

    @classmethod
    def calculate_distance(cls, speed, coords, angle) -> tuple[int, int]:
        rad_angle = np.radians(angle)
        new_x = coords[0] + (speed * np.cos(rad_angle))
        new_y = coords[1] - (speed * np.sin(rad_angle))
        return new_x, new_y

