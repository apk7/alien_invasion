from turtle import right
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_game):
        """Initializing alien and its starting position"""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.fleet_direction = 1
        # Load alien image and resize
        alien_image = pygame.image.load('images/alien.bmp')
        new_width = int(alien_image.get_width() *
                        ai_game.settings.alien_scaling)
        new_height = int(alien_image.get_height() /
                         alien_image.get_width() * new_width)
        self.image = pygame.transform.smoothscale(
            alien_image, (new_width, new_height))

        # Get alien image as a box
        self.rect = self.image.get_rect()

        # Initial position of alien at top-left corner, storing as an attribute
        # adding space to the left-most alien equal to width of alien image
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Storing alien's exact horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def edge_detect(self):
        screen_rect = self.screen.get_rect()
        
        if self.rect.right == screen_rect.right or self.rect.left == 0:
            return True

    def update(self):
        """Moving aliens to right"""
        screen_rect = self.screen.get_rect()

        self.rect.x += (self.settings.alien_fleet_xspeed *
                        self.settings.alien_fleet_direction)