# from cmath import rect
from cmath import rect
from importlib.util import set_loader
import sys
from time import sleep
import pygame
from random import randint

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats
from buttons import Button


class AlienInvasion:
    """Class to manage game assets and behvior"""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        # Starting alien invasion with active state
        self.game_active = False

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

        # Create an instance to store game statistics
        self.stats = GameStats(self)

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

        # Make play button
        self.play_button = Button(self, "PLAY", (0, 255, 0))
        self.reset_button = Button(self, "RESET", (255, 128, 0))

    def run_game(self):
        """Start the main game loop"""
        while True:
            # Helper functions
            # Tracking events
            self._check_events()

            if self.game_active:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_play_button(mouse_position)

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

        elif event.key == pygame.K_p:
            # Exit on pressing "P"
            self.press_p = True
            self._check_play_button()

    def _check_keyup_events(self, event):
        # Ship movement
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _ship_hit(self):
        """Track ship hitting the alien(s)"""

        if self.stats.ships_left > 0:
            # Reducing lives of ship
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet
            self._create_fleet()

            # Initialize ship at the center
            self.ship.center()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False

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
        # Remove alien on colliding with bullet
        self._collision()
        # Recreating fleet once all the aliens are removed
        self._recreat_fleet()

    def _collision(self):
        
        # Check for any bullets that hitted the alien nad remove them
        # pygame.sprite.groupcollide(obj1, obj2,dokill1=True, dokill2=True)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                True, True)   
        if collisions:
            self.stats.score += len(list(collisions.values())[0])
            # self.stats.draw_score(str(self.stats.score))
            # print(list(collisions.values()))
            # print(len(list(collisions.values())[0]))
        
        #Removing bullets that are out of the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

         

    def _recreat_fleet(self):
        """Once all the aliens are killed, recreate the fleet"""       
        # No aliens is present in the "aliens" list
        if not self.aliens:
            # Remove all the bullets from screen
            self.bullets.empty()
            # Create new fleet
            self._create_fleet()
            # Increase downward speed
            self.settings.alien_fleet_yspeed += self.stats.levelup_yspeed
            # Increase the level of the game
            self.stats.level += 1


    
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
            number_aliens = number_aliens_x
            for alien_number in range(number_aliens):
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

        # Alien-Ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print("Game Over !!!")

        # Check if aliens reach bottom of the screen
        self._check_alien_bottom()

    def _check_alien_bottom(self):
        """Check aliens if the aliens have reached bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

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

        # Draw play button if the game is inactive or over:
        if not self.game_active and self.stats.ships_left > 0:
            self.play_button.draw_button()
        elif not self.game_active and self.stats.ships_left == 0:
            self.reset_button.draw_button()

        # Displaying game level and score
        self.stats.draw_level(str(self.stats.level))
        self.stats.draw_score(str(self.stats.score))

        # Making recent most recently drawn screen visible.
        pygame.display.flip()

    ###########################################################################
    # Button: helper functions and methods
    ###########################################################################
    def _check_play_button(self, mouse_pos=(0,0)):
        """Start a new game when the player clicks Play"""

        # To enable the clicking detection only if the play/reset is acive
        button_clicked = (self.play_button.rect.collidepoint(mouse_pos) or
                          self.reset_button.rect.collidepoint(mouse_pos))

        if (button_clicked or self.press_p) and not self.game_active:

            # Resetting stats/lives
            self.stats.reset_stats()

            # Empyting any alien and bullet
            self.aliens.empty()

            self.game_active = True

    ###########################################################################
    # Update and draw gamte statistics
    ###########################################################################
    def _update_level(self):
        # Update level
        self.stats.level += 1

        # render level for displaying
        self.stats.render_level(str(self.stats.level))
        
        # font = pygame.font.Font(None, 36)
        # text = font.render(str(self.stats.level), 1, (0,0,0))
        # textpos = text.get_rect(self.screen.rect.top)
        # self.screen.blit(text, textpos)


if __name__ == '__main__':
    # Creating game instance and runnung the game.
    ai = AlienInvasion()
    ai.run_game()
