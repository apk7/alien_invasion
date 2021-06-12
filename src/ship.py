import pygame
# from settings import Settings

class Ship:
    """Class for creating rocket ship"""
    def __init__(self,ai_game) -> None:
        """Initialize ship with settings"""

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Loading image
        ship_image = pygame.image.load('images/rocket.bmp')
        self.image = pygame.transform.smoothscale(ship_image, 
        (int(ai_game.settings.ship_width), int(ai_game.settings.ship_height))) 

        # Get current image position
        self.rect = self.image.get_rect()

        # Initialize position at the bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Movement
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
        self.ship_speed = ai_game.settings.ship_speed

    def blitme(self):
        """Drawing current position of the ship"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Updating ship's position based of movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ship_speed
            
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x

    def center(self):
        """Centering the ship on the screen once it is deleted"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
