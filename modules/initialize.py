import pygame, sys, logging
from modules.debug import Debug
from modules.boid import Boid

class Initialize:
    def __init__(self) -> None:
        pygame.init()
        self.settings: dict[str, str| int] = self.parse_settings()
        
        try:
            self.screen = pygame.display.set_mode((self.settings['WIDTH'],self.settings['HEIGHT'])) 
        except KeyError as e:
            logging.error(f"{e}: No value for HEIGHT or WIDTH in config found.")
            sys.exit()

        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Boid Simulation")
        boid_icon = pygame.image.load("graphics/Icon.png").convert_alpha()
        pygame.display.set_icon(boid_icon)

    def run(self):
        boid = Boid(self.settings)
        # A list that will hold all postions of the boids
        positions: list[tuple[int, int]] = list()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                # Adding a boid for every mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    boid.generate(pygame.mouse.get_pos())

            # Debug Messages
            message_list: list[str] = list()

            self.screen.fill("black")

            boi_list: list = list()
            for boid_properties in boid.renderable():
                self.screen.blit(boid_properties["surface"], boid_properties["rectangle"])
                boi_list.append((boid_properties["rectangle"], boid_properties["rotation"]))

            message_list.append(f"{boi_list=}")
            message_list.append(f"boid_count={len(boi_list)}")

            Debug(message_list, self.screen)

            pygame.display.update()

            try:
                self.clock.tick(self.settings['FPS'])
            except KeyError as e:
                logging.error(f"{e}: No FPS value in config found.")
                sys.exit()

    def parse_settings(self):
        # Get root directory by splitting __file__ at '/' twice and 
        # getting value at first index
        root: str = __file__.rsplit("/", 2)[0]

        options: dict = {}

        with open(root + '/' + "settings.ini", "r") as settings_file:
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

def main():
    ...

if __name__ == "__main__":
    main()

