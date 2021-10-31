from pyskier.get_images import GetImages
from pygame import image, sprite

class SkierSprite(sprite.Sprite):
    """ Skier sprite class"""

    def __init__(self, path):
        sprite.Sprite.__init__(self)
        self.images_path = path
        self.image = image.load(f"{self.images_path}skier_down.png")
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.angle = 0

    def turn(self, direction):
        """ Load new image and change speed when the skier turns.
        Returns speed value. 
        """

        self._skier_images = GetImages(self.images_path).sort_images()

        self.angle = self.angle + direction
        if self.angle < -2:  self.angle = -2
        if self.angle > 2:  self.angle = 2

        center = self.rect.center
        self.image = image.load(f"{self.images_path}{self._skier_images[self.angle]}")
        self.rect = self.image.get_rect()
        self.rect.center = center

        self._speed = [self.angle, 6 - abs(self.angle) * 2]
        return self._speed

    def move(self, speed):
        """ Move the skier right and left. """

        self.rect.centerx = self.rect.centerx + speed[0]
        if self.rect.centerx < 20:  self.rect.centerx = 20
        if self.rect.centerx > 620: self.rect.centerx = 620


class ObstacleSprite(sprite.Sprite):
    """ Obstacle sprites (trees & flags) class. """

    def __init__(self, image_file, location, obstacle_type):
        sprite.Sprite.__init__(self)
        self.image_file = image_file
        self.image = image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = obstacle_type
        self.passed = False

    def update(self, speed):
        """ Update obstacles according to speed."""
        
        self.rect.centery -= speed[1]
        if self.rect.centery < -32:
            self.kill()


if __name__ == "__main__":
    # Skier images folder path.
    images_folder = '../images/'