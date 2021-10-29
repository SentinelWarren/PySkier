# PySkier
# Copyright Warren & Carter Sande, 2013
# Released under MIT license   http://www.opensource.org/licenses/mit-license.php
# Version 1.00

from get_images import GetImages
import pygame, random

# Skier images folder path.
images_folder = '../images/'

# Get custom sorted image names.
get_images = GetImages(images_folder)
skier_images = get_images.sort_images()

class SkierClass(pygame.sprite.Sprite):
    """ Skier sprite class"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f"{images_folder}skier_down.png")
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.angle = 0

    def turn(self, direction):
        """ load new image and change speed when the skier turns. """

        self.angle = self.angle + direction
        if self.angle < -2:  self.angle = -2
        if self.angle > 2:  self.angle = 2
        center = self.rect.center
        self.image = pygame.image.load(f"{images_folder}{skier_images[self.angle]}")
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed = [self.angle, 6 - abs(self.angle) * 2]
        return speed

    def move(self, speed):
        """ move the skier right and left. """

        self.rect.centerx = self.rect.centerx + speed[0]
        if self.rect.centerx < 20:  self.rect.centerx = 20
        if self.rect.centerx > 620: self.rect.centerx = 620


class ObstacleClass(pygame.sprite.Sprite):
    """ Obstacle sprites (trees & flags) class. """

    def __init__(self, image_file, location, type):
        pygame.sprite.Sprite.__init__(self)
        self.image_file = image_file
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type
        self.passed = False

    def update(self):
        global speed
        self.rect.centery -= speed[1]
        if self.rect.centery < -32:
            self.kill()


def create_map():
    """ Creates one 'screen' of obstacles; 640 x 640 
    use "blocks" of 64 x 64 pixels, so objects aren't too close together.
    """

    global obstacles
    locations = []
    for _i in range(10):  # 10 obstacles per screen
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        location = [col * 64 + 32, row * 64 + 32 + 640]  # center x, y for obstacle
        if not (location in locations):  # prevent 2 obstacles in the same place
            locations.append(location)
            type = random.choice(["tree", "flag"])
            if type == "tree":
                img = f"{images_folder}skier_tree.png"
            elif type == "flag":
                img = f"{images_folder}skier_flag.png"
            obstacle = ObstacleClass(img, location, type)
            obstacles.add(obstacle)


def animate():
    """ redraw the screen, including all sprites. """

    screen.fill([255, 255, 255])
    obstacles.draw(screen)
    screen.blit(skier.image, skier.rect)
    screen.blit(score_text, [10, 10])
    pygame.display.flip()


# initialize everything
pygame.init()
screen = pygame.display.set_mode([640, 640])
clock = pygame.time.Clock()
speed = [0, 6]
obstacles = pygame.sprite.Group()  # group of obstacle objects
skier = SkierClass()
map_position = 0
points = 0
create_map()  # create one screen full of obstacles
font = pygame.font.Font(None, 50)

# main Pygame event loop
running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

        if event.type == pygame.KEYDOWN:  # check for key presses
            if event.key == pygame.K_LEFT:  # left arrow turns left
                speed = skier.turn(-1)
            elif event.key == pygame.K_RIGHT:  # right arrow turns right
                speed = skier.turn(1)
    skier.move(speed)  # move the skier (left or right)
    map_position += speed[1]  # scroll the obstacles

    # create a new block of obstacles at the bottom
    if map_position >= 640:
        create_map()
        map_position = 0

    # check for hitting trees or getting flags
    hit = pygame.sprite.spritecollide(skier, obstacles, False)
    if hit:
        if hit[0].type == "tree" and not hit[0].passed:  # crashed into tree
            points = points - 100
            skier.image = pygame.image.load(f"{images_folder}skier_crash.png")  # crash image
            animate()
            pygame.time.delay(1000)
            skier.image = pygame.image.load(f"{images_folder}skier_down.png")  # resume skiing
            skier.angle = 0
            speed = [0, 6]
            hit[0].passed = True
        elif hit[0].type == "flag" and not hit[0].passed:  # got a flag
            points += 10
            hit[0].kill()  # remove the flag

    obstacles.update()
    score_text = font.render("Score: " + str(points), 1, (0, 0, 0))
    animate()

pygame.quit()
