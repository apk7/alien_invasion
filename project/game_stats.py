import pygame.font
# For tracking game sttistics

class GameStats:
    """Tracking statistics for the game"""

    def __init__(self, ai_game):
        """Initialize class"""
        self.settings = ai_game.settings
        self.reset_stats()

        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.font = pygame.font.SysFont(None, 25)
        # Build the rect object and center it
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.top = self.screen_rect.top
        
    def reset_stats(self):
        """Resetting game statistics"""

        # lives of player in the game (change the name to lives)
        self.ships_left = self.settings.ship_limit
        self.level =  self.settings.stat_level
        self.score =  self.settings.stat_score
        self.levelup_yspeed = self.settings.stat_levelup_yspeed

    # def render_level(self, msg):
    #     """Turning text into rendered image and ceter the text on button"""
    #     self.msg_image = self.font.render(msg, True, (0,0,0),
    #                                       (255,255,255))
    #     self.msg_image_rect = self.msg_image.get_rect()
    #     self.msg_image_rect.top = self.rect.top
    
    def draw_level(self,msg):
        self.msg_image = self.font.render("Level - " + msg, True, (255,128,0),
                                          self.settings.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.left = self.screen_rect.left + 20
        self.msg_image_rect.top = self.screen_rect.top + 5
        # self.screen.fill((255,255,255), self.rect)
        # print(self.screen_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def draw_score(self,msg):
        self.msg_image = self.font.render("Score - " + msg, True, (51,255,255),
                                          self.settings.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.right = self.screen_rect.right-20
        self.msg_image_rect.top = self.screen_rect.top + 5
        # self.screen.fill((255,255,255), self.rect)
        # print(self.screen_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        