class Settings:
    """Settings of the game"""

    def __init__(self) -> None:
        """Initializing game settings"""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 26, 56)

        # Ship settings
        self.ship_width = self.screen_width*0.08
        self.ship_height = self.ship_width * \
            (self.screen_width/self.screen_height) * 0.7
        self.ship_speed = 1

        # Bullets settings
        self.bullet_speed = 1.0
        self.bullet_allowed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)


        # Alien settings
        self.alien_scaling = 0.05

        # Star settings
        self.star_numbers = 150
        self.star_scale = 0.025
        self.star_speed = 2
        