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
        # Timer to update the boids
        update_boid_timer = pygame.USEREVENT + 1
        # Triggers every 100 miliseconds
        pygame.time.set_timer(update_boid_timer, 100)

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

            # Debug Messages
            message_list: list[str] = list()

            self.screen.fill("black")

            boid_list: list = list()
            for boid_properties in boid.renderable():
                self.screen.blit(boid_properties["surface"], boid_properties["rectangle"])
                boid_list.append((boid_properties["rectangle"], boid_properties["rotation"]))

            for i in range(len(boid_list)):
                message_list.append(f"boid_list={boid_list[i][0].center}, {round(boid_list[i][1], 2)}")
            message_list.append(f"boid_count={len(boid_list)}")
            message_list.append(f"mouse_pos={pygame.mouse.get_pos()}")

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

