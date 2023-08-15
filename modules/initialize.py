import pygame, sys
from modules.debug import Debug
from modules.boid import Boid

class Initialize:
    def __init__(self) -> None:
        pygame.init()
        self.settings: dict[str, str| int] = self.parse_settings()
        self.validate_settings()
        
        self.screen = pygame.display.set_mode((self.settings['WIDTH'],self.settings['HEIGHT'])) 

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Boid Simulation")
        boid_icon = pygame.image.load("graphics/Icon.png").convert_alpha()
        pygame.display.set_icon(boid_icon)

    def run(self):
        # Timer to update the boids
        # Triggers every 100 miliseconds
        update_boid_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(update_boid_timer, 100)

        # Timer to reload config
        # Reloads every 2 seconds
        reload_config_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(reload_config_timer, 2000)

        boid = Boid(self.settings)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Adding a boid for every mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    left_clicked, middle_clicked, right_clicked = pygame.mouse.get_pressed()
                    if left_clicked and not(middle_clicked or right_clicked):
                        boid.generate(pygame.mouse.get_pos())

                # Add boid everytime spacebar is pressed
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        boid.generate(pygame.mouse.get_pos())

                # Update boid properties everytime update_boid_timer is triggered
                # that is boid properties are updated every 100 miliseconds
                if event.type == update_boid_timer:
                    boid.update_properties(pygame.mouse.get_pos())

                # Reload settings values everytime reload_config_timer is triggered
                # Values are realoaded every 2 seconds
                if event.type == reload_config_timer:
                    self.settings: dict[str, str| int] = self.parse_settings()
                    self.validate_settings()
                    boid.update_settings(self.settings)

            # Debug Messages
            message_list: list[str] = list()

            self.screen.fill("black")

            boid_list = boid.get_renderable()
            boid_perception_fields = boid.get_perception_fields()

            for entry in boid_perception_fields:
                pygame.draw.circle(self.screen, entry["color"], entry["coords"], self.settings["RADIUS"])

            for boid_properties in boid_list:
                self.screen.blit(boid_properties["surface"], boid_properties["rectangle"])

            message_list.append(f"mouse_pos={pygame.mouse.get_pos()}")
            message_list.append(f"boid_count={len(boid_list)}")
            for i in range(len(boid_list)):
                message_list.append(f"boid_{i}={boid_list[i]['rectangle'].center}, {round(boid_list[i]['rotation'], 2)}")

            # Display all debug messages on the screen surface
            Debug(message_list, self.screen)

            pygame.display.update()

            self.clock.tick(self.settings['FPS'])

    def parse_settings(self) -> dict[str, int | str]:
        # Get root directory by splitting __file__ at '/' twice and 
        # getting value at first index
        root_dir: str = __file__.rsplit("/", 2)[0]

        options: dict = {}

        # TODO: Hardcode default settings file
        with open(root_dir + '/' + "settings.ini", "r") as settings_file:
            lines_list: list = settings_file.read().split('\n')

            for line in lines_list:
                # Only parse furthur if line is not empty
                if line != '':
                    # Remove all whitespaces from line and get first character
                    line_1st_char: str = line.strip()[0]

                    if line_1st_char != '[':
                        try:
                           options[line.split('=')[0].strip()] = int(line.split('=')[1].strip())
                        except ValueError:
                           options[line.split('=')[0].strip()] = line.split('=')[1].strip()
        return options

    def validate_settings(self):
        valid_settings: list[str] = ["HEIGHT", "WIDTH", "FPS", "RADIUS", "SPEED", "ICONPATH"]
        for value in valid_settings:
            if value not in self.settings.keys():
                print(f"{value} not found in settings.ini")
                sys.exit()

def main() -> None:
    ...

if __name__ == "__main__":
    main()

