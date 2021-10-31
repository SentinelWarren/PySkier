# PySkier
# Copyright Warren & Carter Sande, 2013
# Released under MIT license   http://www.opensource.org/licenses/mit-license.php
# Version 1.00

from pyskier.sprites import SkierSprite, ObstacleSprite
import pygame, random

class SkierGame():
    """ Main Game class. """

    def __init__(self, path):
        self.images_path = path
        self.obstacles = pygame.sprite.Group()  # group of obstacle objects
        self.skier = SkierSprite(self.images_path)

    def _create_map(self):
        """ Creates one 'screen' of obstacles; 640 x 640 
        use "blocks" of 64 x 64 pixels, so objects aren't too close together.
        """

        self._locations = []
        for _ in range(10):  # 10 obstacles per screen
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            
            location = [col * 64 + 32, row * 64 + 32 + 640]  # center x, y for obstacle
            if not (location in self._locations):  # prevent 2 obstacles in the same place
                self._locations.append(location)
                
                obstacle_type = random.choice(["tree", "flag"])
                if obstacle_type == "tree":
                    img = f"{self.images_path}skier_tree.png"
                elif obstacle_type == "flag":
                    img = f"{self.images_path}skier_flag.png"
                
                obstacle = ObstacleSprite(img, location, obstacle_type)
                self.obstacles.add(obstacle)

    def _animate(self):
        """ Redraw the screen, including all sprites. """

        self._screen = pygame.display.set_mode([640, 640])
        self._screen.fill([255, 255, 255])
        self.obstacles.draw(self._screen)
        
        self._screen.blit(self.skier.image, self.skier.rect)
        self._screen.blit(self._score_text, [10, 10])
        pygame.display.flip()

    def run(self):
        """ main Pygame event loop """

        pygame.init()
        clock = pygame.time.Clock()
        speed = [0, 6]
        map_position = 0
        points = 0
        self._create_map()  # create one screen full of obstacles
        font = pygame.font.Font(None, 50)

        running = True
        while running:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False

                if event.type == pygame.KEYDOWN:  # check for key presses
                    if event.key == pygame.K_LEFT:  # left arrow turns left
                        speed = self.skier.turn(-1)
                    elif event.key == pygame.K_RIGHT:  # right arrow turns right
                        speed = self.skier.turn(1)
            
            self.skier.move(speed)  # move the skier (left or right)
            map_position += speed[1]  # scroll the obstacles

            # create a new block of obstacles at the bottom
            if map_position >= 640:
                self._create_map()
                map_position = 0

            # check for hitting trees or getting flags
            hit = pygame.sprite.spritecollide(self.skier, self.obstacles, False)
            if hit:
                if hit[0].type == "tree" and not hit[0].passed:  # crashed into tree
                    points = points - 50
                    
                    self.skier.image = pygame.image.load(f"{self.images_path}skier_crash.png")  # crash image
                    self._animate()
                    pygame.time.delay(1000)
                    self.skier.image = pygame.image.load(f"{self.images_path}skier_down.png")  # resume skiing
                    self.skier.angle = 0
                    speed = [0, 6]
                    hit[0].passed = True
                elif hit[0].type == "flag" and not hit[0].passed:  # got a flag
                    points += 10
                    hit[0].kill()  # remove the flag

            self.obstacles.update(speed)
            self._score_text = font.render("Score: " + str(points), 1, (0, 0, 0))
            self._animate()

    def quit(self):
        pygame.quit()


if __name__ == "__main__":
    
    # Play the game
    skier_game = SkierGame('../images/')
    skier_game.run()
    skier_game.quit()
