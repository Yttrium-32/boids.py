import pygame, sys
from modules.boid import Boid

class Initialize:
    def __init__(self) -> None:
        pygame.init()
        self.settings: dict[str, str | int] = self.parse_settings()
        self.validate_settings()
        
        self.screen = pygame.display.set_mode((self.settings['WIDTH'],self.settings['HEIGHT']))

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Boid Simulation")
        boid_icon = pygame.image.load("graphics/Icon.png").convert_alpha()
        pygame.display.set_icon(boid_icon)

    def run(self):
        boid = Boid()

        # Main rendering loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill("black")

            boid.draw(self.screen)
            boid.update()

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
        valid_settings: set[str] = {"HEIGHT", "WIDTH", "FPS", "RADIUS", "SPEED", "ICONPATH"}
        for value in valid_settings:
            if value not in self.settings.keys():
                print(f"{value} not found in settings.ini")
                sys.exit()

