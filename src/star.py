import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    """Class for stars in the background"""

    def __init__(self, ai_game):
        """Initializing star class"""
        
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load and scale star image
        star_image = pygame.image.load('images/star.bmp')
        scaling_factor = ai_game.settings.star_scale
        new_width = int(star_image.get_width() * scaling_factor)
        self.image = pygame.transform.smoothscale(star_image,
                                                  (new_width, new_width))

        # Get image as a box
        self.rect = self.image.get_rect()

        # Random position of stars
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

    def update(self):
        """Move stars"""
        # Update position of the bullet
        self.rect.y += self.settings.star_speed

        # Update rectangle position
        # self.rect.y = self.y