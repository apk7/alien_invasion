class Settings:
    """Settings of the game"""

    def __init__(self) -> None:
        """Initializing game settings"""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        # self.bg_color = (0, 5, 10)
        self.bg_color = (0, 13, 20)

        # Ship settings
        self.ship_width = self.screen_width*0.08
        self.ship_height = self.ship_width * \
            (self.screen_width/self.screen_height) * 0.7
        self.ship_speed = 1
        self.ship_limit = 3 # lives

        # Bullets settings
        self.bullet_speed = 1.0
        self.bullet_allowed = 5
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        # Alien settings
        self.alien_scaling = 0.05
        self.alien_fleet_direction = 1
        self.alien_fleet_xspeed = 1.0
        self.alien_fleet_yspeed = 3

        # Star settings
        self.star_numbers = 150
        self.star_scale = 0.025
        self.star_speed = 2

        # Game stats initial setting
        self.stat_level = 0
        self.stat_score = 0
        self.stat_levelup_yspeed = 3
        self.stat_color_level = (255, 128, 0)
        self.stat_color_score = (51, 255, 255)
        self.stat_color_lives = (255, 102, 102)
