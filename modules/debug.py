from re import L
import pygame
import pygame.freetype

class Debug:
    # Coordinates to render the first debug message
    default_message_coords: tuple = (1, 1)
     
    def __init__(self, message_list: list, screen: pygame.Surface) -> None:
        font = pygame.freetype.Font(None, 12)
        debug_count: int = 0
        message_coords: list = []

        for debug_message in message_list:
            debug_count += 1

            for _ in range(debug_count):
                message_coords = [Debug.default_message_coords[0], Debug.default_message_coords[1] * debug_count * 10]

            message_surface = font.render(text=debug_message, fgcolor="white", bgcolor="black")
            screen.blit(message_surface[0], message_coords)

