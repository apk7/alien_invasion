import pygame.font
import sys


class GameStats:
    """Tracking statistics for the game"""

    def __init__(self, ai_game):
        """Initialize class"""
        self.settings = ai_game.settings
        self.reset_stats()

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.font = pygame.font.SysFont("segoe-ui-symbol", 20)
        # Build the rect object and center it
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.top = self.screen_rect.top

    def reset_stats(self):
        """Resetting game statistics"""

        # lives of player in the game (change the name to lives)
        self.ships_left = self.settings.ship_limit
        self.level = self.settings.stat_level
        self.score = self.settings.stat_score
        self.levelup_yspeed = self.settings.stat_levelup_yspeed

    def draw_stats(self, msg, color, stat_pos):
        """Drawing stats for level, score and lives.
        msg:        Message that needs to be shown
        color:      Color of the text
        stat_pos:   Text position.[top_left, top_center, top_right]
        """
        self.msg_image = self.font.render(msg, True, color,
                                          self.settings.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()

        # Text position
        if stat_pos == "top_left":
            self.msg_image_rect.left = self.screen_rect.left + 20
        elif stat_pos == "top_center":
            self.msg_image_rect.center = self.screen_rect.center
        elif stat_pos == "top_right":
            self.msg_image_rect.right = self.screen_rect.right - 20

        self.msg_image_rect.top = self.screen_rect.top + 5
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_game_over(self):
        # Load game over image and resize
        image = pygame.image.load('images/game_over.bmp')
        new_width = int(image.get_width() * 0.5)
        new_height = int(image.get_height() /
                         image.get_width() * new_width)
        self.image = pygame.transform.smoothscale(image,
                                                  (new_width, new_height))

        # Get alien image as a box
        self.rect = self.image.get_rect()

        # Initial position of alien at top-left corner, storing as an attribute
        # adding space to the left-most alien equal to width of alien image
        # print(help(self.screen_rect))
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery - 100
        # self.rect.centery = 20
        self.screen.blit(self.image, self.rect)
        


# pygame.font.match_font
# str = "♛" * 5
# print(str)
