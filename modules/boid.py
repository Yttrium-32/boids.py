import pygame
import numpy as np
from random import randint

class Boid:
    def __init__(self, settings: dict[str, str | int]) -> None:
        self.settings = settings
        boid_surface = pygame.image.load(settings["ICONPATH"])
        self.boid_surface = pygame.transform.scale(boid_surface, (50,50))
        self.boid_list: list[dict] = list()
        self.wrap: bool = 0
            
    def get_renderable(self):
        boid_properties_list: list[dict] = list()
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

            boid_properties_list.append(boid_properties)

        return boid_properties_list

    def generate(self, coords: tuple[int, int]):
        boid_rotation = randint(0, 360)
        boid_rect = self.boid_surface.get_rect(center = coords)
        self.boid_list.append({"rectangle": boid_rect, "rotation": boid_rotation, "coords": coords})

    def update_properties(self):
        for boid_index in range(len(self.boid_list)):

            # Changing angle of each boid in boid_list
            angle = self.boid_list[boid_index]["rotation"]

            steering_angle = self.align(boid_index)
            angle += steering_angle

            self.boid_list[boid_index]["rotation"] = angle
            if self.boid_list[boid_index]["rotation"] >= 360:
                self.boid_list[boid_index]["rotation"] = self.boid_list[boid_index]["rotation"] - 360

            current_rect = self.boid_list[boid_index]["rectangle"]

            self.boid_list[boid_index]["rectangle"] = self.calculate_new_rect(current_rect, angle)
            self.boid_list[boid_index]["coords"] = self.boid_list[boid_index]["rectangle"].center

    def calculate_new_rect(self, current_rect: pygame.Rect, angle: int):
        new_rect: pygame.Rect = current_rect
        center_coords = current_rect.center
        new_coords = calculate_distance(self.settings["SPEED"], center_coords, angle)
        new_rect.center: tuple[int, int] = new_coords

        # Screen wrap implementation
        if not self.wrap:
            # Screen wrap vertically
            if new_rect.x >= self.settings["WIDTH"]:
                new_rect.x -= self.settings["WIDTH"]  
                self.wrap: bool = True
            if new_rect.x <= 0:
                new_rect.x = self.settings["WIDTH"]
                self.wrap: bool = True

            # Screen wrap horizontally
            if new_rect.y >= self.settings["HEIGHT"]:
                new_rect.y -= self.settings["HEIGHT"]
                self.wrap: bool = True
            if new_rect.y <= 0:
                new_rect.y = self.settings["HEIGHT"]
                self.wrap: bool = True
        else:
            self.wrap: bool = False

        return new_rect

    def get_perception_fields(self):
        perception_field_list: dict[str, int] = []
        for boid in self.boid_list:
            perceived_boids_list: list[int] = list()
            color = "#111111"
            current_boid_index = self.boid_list.index(boid)

            for other_boid in self.boid_list:

                other_boid_index = self.boid_list.index(other_boid)
                if other_boid_index != current_boid_index:

                    current_boid_x = boid["rectangle"].x 
                    current_boid_y = boid["rectangle"].y

                    other_boid_x = other_boid["rectangle"].x
                    other_boid_y = other_boid["rectangle"].y

                    dist = np.sqrt((current_boid_x - other_boid_x) ** 2 + (current_boid_y - other_boid_y) ** 2)
                    
                    if dist < self.settings["RADIUS"]:
                        perceived_boids_list.append(other_boid_index)

            if perceived_boids_list != []:
                color = "#F33329"

            perception_field_list.append({"coords": boid["rectangle"].center, "color": color, "perceived": perceived_boids_list})

        return perception_field_list

    def align(self, boid_index: int):
        perception_field_list = self.get_perception_fields()
        perceived_boids: list[int] = []
        for field in perception_field_list:
            if field["coords"] == self.boid_list[boid_index]["coords"]:
                perceived_boids = field["perceived"]

        sum_of_angles: int = 0
        for index in perceived_boids:
            sum_of_angles += self.boid_list[index]["rotation"]

        if sum_of_angles > 0:
            average_angle = sum_of_angles / len(self.boid_list[index])
            current_angle = self.boid_list[boid_index]["rotation"]
            steering_angle = average_angle - current_angle
        else: steering_angle = 0

        return steering_angle

    def update_settings(self, new_settings):
        self.settings = new_settings


def calculate_distance(speed, coords, angle) -> tuple[int, int]:
    rad_angle = np.radians(angle)
    new_x = coords[0] + (speed * np.cos(rad_angle))
    new_y = coords[1] - (speed * np.sin(rad_angle))
    return new_x, new_y

