from cmath import rect
import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from random import randint


class AlienInvasion:
    """Class to manage game assets and behvior"""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        # Get settings
        self.settings = Settings()

        # Screen settings
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        # # Full screen settings
        # # Get full-screen data
        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # # Set full-screen data
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        # Assigning ship attributes
        self.ship = Ship(self)

        # Assigning bullet attributes
        self.bullets = pygame.sprite.Group()

        # Create aliens
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Create stars
        self.stars = pygame.sprite.Group()
        self._create_stars_group()

    def run_game(self):
        """Start the main game loop"""
        while True:
            # Helper functions
            # Tracking events
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_stars()
            self._update_aliens()
            self._update_screen()

    ###########################################################################
    # Events: helper functions and methods
    ###########################################################################
    def _check_events(self):
        # Tracking keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # Ship movement
        if event.key == pygame.K_RIGHT:
            # Moving ship to right
            self.ship.moving_right = True
            self.ship.moving_left = False
        elif event.key == pygame.K_LEFT:
            # Moving ship to left
            self.ship.moving_left = True
            self.ship.moving_right = False

        elif event.key == pygame.K_q:
            # Exit on pressing "Q"
            sys.exit()

        elif event.key == pygame.K_SPACE:
            # Firing bullets
            self._fire_bullets()

    def _check_keyup_events(self, event):
        # Ship movement
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    ###########################################################################
    # Bullets: helper functions and methods
    ###########################################################################
    def _fire_bullets(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Updating bullet location and removing out-of-screen bullets"""
        self.bullets.update()
        # Removing bullets that are out of the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    ###########################################################################
    # Aliens: helper functions and methods
    ###########################################################################
    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Make an alien
        alien = Alien(self)

        # Getting number of aliens in a row
        # |←one alien margin→ (a_0)←0.5 a_x gap →(a_1)...(a_x)←one alien margin→|
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        aliens_gap_x = alien_width/0.75
        number_aliens_x = int(available_space_x //
                              (alien_width + aliens_gap_x))

        # Getting number of aliens in a column
        alien_height = alien.rect.height
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (16 * alien_height) - ship_height)
        aliens_gap_y = alien_height/0.75
        number_aliens_y = int(available_space_y //
                              (alien_height + aliens_gap_y))

        # Creating first row of element
        for row_number in range(number_aliens_y):
            # if row_number%2!=0:
            #     number_aliens = number_aliens_x-2
            # else:
            number_aliens = number_aliens_x
            for alien_number in range(number_aliens):
                # if row_number%2!=0 and alien_number%2==0:
                #     continue
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row
        alien = Alien(self)

        alien_width, alien_height = alien.rect.size
        aliens_gap_x = alien_width/0.75
        aliens_gap_y = alien_height/0.75

        alien.x = alien_width + (alien_width + aliens_gap_x) * alien_number
        alien.rect.x = alien.x

        alien.y = alien_height + (alien_height + aliens_gap_y) * row_number
        alien.rect.y = alien.y

        self.aliens.add(alien)

    def _update_aliens(self):
        """Change position on detecting edges"""
        
        for alien in self.aliens.sprites():
            # Detect if any alien detects the edge
            if alien.edge_detect():
                for alien in self.aliens.sprites():
                    # Dropping
                    alien.rect.y += self.settings.alien_fleet_yspeed
                # Changing direction
                self.settings.alien_fleet_direction *= -1
                # breaking loop: even if one alien detects edge all the
                # parameters for whole fleet is changed
                break
        # Updating the whole fleet
        self.aliens.update()    
            
               
    
    # def _change_fleet
    #     self.aliens.update()

    ###########################################################################
    # Star: helper functions and methods
    ###########################################################################
    def _create_stars_group(self):
        """Creating stars"""

        for number in range(0, self.settings.star_numbers):
            self._create_stars()

    def _create_stars(self):
        star = Star(self)
        star.rect.x = randint(0, self.settings.screen_width)
        star.rect.y = randint(0, self.settings.screen_height)
        self.stars.add(star)

    def _update_stars(self):
        """Updating bullet location and removing out-of-screen stars"""
        self.stars.update()


        # Removing bullets that are out of the screen
        for star in self.stars.copy():
            if star.rect.bottom >= self.settings.screen_height:
                self.stars.remove(star)
                self._create_stars()

    ###########################################################################
    # Update: helper functions and methods
    ###########################################################################
    def _update_screen(self):
        # Redrawing screen with background color
        self.screen.fill(self.settings.bg_color)

        # Draw star
        self.stars.draw(self.screen)

        # Drawing ship
        self.ship.blitme()

        # Draw bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw alien
        self.aliens.draw(self.screen)

        # Making recent most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Creating game instance and runnung the game.
    ai = AlienInvasion()
    ai.run_game()
