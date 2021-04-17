import sys
import json
import os

from time import sleep
from datetime import datetime

import pygame
from pygame.mixer import Sound

# Data structures
from settings import Settings
from game_stats import GameStats

# Graphic assets
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

# Configuration menu
from ini_config import conff_menu


class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self, configuration, main_path):
        """Initialize the game, and create game resources"""
        pygame.init()

        ####################################################################################
        # System configuration
        ####################################################################################

        # Current user.
        self.user = configuration[0]

        # Path for the game assets and user data.
        self.path = main_path
        self.high_scores_filename = self.path + "user_data/high_scores.json"
        self.saved_games_filename = self.path + "user_data/saved_games.json"

        # Set initial difficulty and general settings.
        self.ini_diff = configuration[1]
        self.settings = Settings(self.ini_diff)

        # Configure screen.
        self.screen_size = configuration[2]
        if self.screen_size == "Full Screen":
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height)
            )
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        high_score = self._retrive_high_score()
        self.stats = GameStats(self, high_score)

        # Create a Scoreboard to display score and level data on the screen.
        self.sb = Scoreboard(self)

        ####################################################################################
        # Game assets.
        ####################################################################################

        # Load sound effects.
        self._load_sound_effects()

        # Create an instance for a ship and groups for bullets and aliens.
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Saved game?
        if configuration[3]:
            self.saved_game = True
        else:
            self.saved_game = False
            # Create the fleet of aliens if this is a new game.
            self._create_fleet()

        ####################################################################################
        # Load saved game state
        ####################################################################################

        if self.saved_game:
            saved_game = configuration[3]

            # Scores.
            self.stats.ships_left = saved_game["ship_left"]
            self.sb.prep_ships()
            self.stats.score = saved_game["current_score"]
            self.sb.prep_score()
            self.stats.level = saved_game["level"]
            self.sb.prep_level()

            # Speeds.
            self.settings.ship_speed = saved_game["ship_speed"]
            self.settings.bullet_speed = saved_game["bullet_speed"]
            self.settings.alien_speed = saved_game["alien_speed"]
            self.settings.alien_points = saved_game["alien_points"]
            self.settings.fleet_direction = saved_game["fleet_direction"]

            # Screen state.
            self.ship.x = saved_game["ship_x"]
            self.ship.rect.x = int(self.ship.x)
            self._get_saved_fleet(saved_game["aliens"], self.aliens)

        ####################################################################################
        # Buttons
        ####################################################################################

        # Play button.
        self.play_button = Button(
            msg="Play",
            main_path=main_path,
            b_width="auto",
        )

        # Resume button.
        self.resume_button = Button(
            msg="Resume",
            main_path=main_path,
            pos_y=self.screen_rect.centery + (60 if self.user != "anon" else 30),
        )

        # Quit button.
        self.quit_button = Button(
            msg="Quit",
            main_path=main_path,
            pos_y=self.screen_rect.centery - (60 if self.user != "anon" else 30),
        )

        # Game won.
        self.won_button = Button(
            msg="You won the game!",
            main_path=main_path,
            b_width="auto",
        )

        # If user is anonymous, don't offer save option.
        if self.user != "anon":
            # Save button.
            self.save_button = Button(
                msg="Save",
                main_path=main_path,
                pos_y=self.screen_rect.centery,
            )

    ########################################################################################
    # Set-up functions
    ########################################################################################

    def _get_saved_fleet(self, saved_fleet, new_fleet):
        """Load saved alien fleet"""
        for item in saved_fleet:
            alien = Alien(self)
            alien.x = item["x"]
            alien.rect.y = item["y"]
            alien.rect.x = int(alien.x)
            new_fleet.add(alien)

    def _load_sound_effects(self):
        """Load sound files for the game sound effects"""

        # Set ambient sound and reduce its volume to be less annoying.
        self.ambient_sound = Sound(self.path + "sounds/ambient.wav")
        self.ambient_sound.set_volume(0.5)

        # Set other sounds effects.
        self.loose_ship_sound = Sound(self.path + "sounds/loose_ship.wav")
        self.laser_sound = Sound(self.path + "sounds/laser.wav")
        self.click_sound = Sound(self.path + "sounds/click.wav")
        self.fail_shot = Sound(self.path + "sounds/fail_shot.wav")
        self.game_won_sound = Sound(self.path + "sounds/game_won.wav")
        self.game_won_sound.set_volume(2)

    def _retrive_high_score(self):
        """Retrive user highest past score"""
        if self.user == "anon":
            return 0
        else:
            try:
                with open(self.high_scores_filename) as f:
                    score = json.load(f)
                return score[self.user]["high_score"]
            except FileNotFoundError:
                return 0

    def _create_fleet(self):
        """Create the fleet of aliens"""

        # Create an alien and find its size and the height of the ship.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height

        # Determine the number of columns of aliens that fit on the screen,
        # spacing between each alien is equal to one alien width.
        available_space_x = self.screen_rect.width - (2 * alien_width)
        number_columns = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen,
        # spacing between each alien is equal to one alien height.
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for column_number in range(number_columns):
                self._create_alien(column_number, row_number)

    def _create_alien(self, column_number, row_number):
        """Create an alien and place it in the corresponding position"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * column_number
        alien.rect.y = alien_height + 2 * alien_height * row_number
        alien.rect.x = alien.x
        self.aliens.add(alien)

    ########################################################################################
    # Run-time functions
    ########################################################################################

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            restart = self._check_events()

            # If the players won the game and clicks
            # on the screen, go back to the main menu.
            if restart:
                return None

            if self.stats.game_active and not self.stats.game_pause:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            if not self.stats.game_end:
                self._update_screen()

            if self.stats.level > 50 and self.stats.game_active:
                self._show_won_game_message()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""

        # Background color.
        self.screen.fill(self.settings.bg_color)

        # Draw ship.
        self.ship.blitme()

        # Draw bullets.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw aliens.
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw buttons.
        if self.stats.game_pause:
            self.resume_button.draw_button(self.screen)
            self.quit_button.draw_button(self.screen)
            # If user is anonymous, don't offer save option.
            if self.user != "anon":
                self.save_button.draw_button(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button(self.screen)

        pygame.display.flip()

    ########################################################################################
    # User-actions functions
    ########################################################################################

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit_game()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                restart = self._check_keydown_events(event)
                if restart == "restart":
                    return "restart"
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.stats.game_active:
                    if self.stats.game_end:
                        restart = self._check_end_button(mouse_pos)
                        if restart:
                            return "restart"
                    else:
                        self._check_play_button(mouse_pos)
                if self.stats.game_pause:
                    restart = self._check_pause_buttons(mouse_pos)
                    if restart == "restart":
                        return "restart"

    def _check_keydown_events(self, event):
        """Respond to keypresses"""

        # Game actions.
        if event.key == pygame.K_RIGHT and self.stats.game_active:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT and self.stats.game_active:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()

        # Start-stop game.
        elif event.key == pygame.K_q:
            return self._exit_game()
        elif event.key == pygame.K_s:
            if not self.stats.game_active and not self.stats.game_end:
                self._start_game()
        elif event.key == pygame.K_p:
            if self.stats.game_active and not self.stats.game_pause:
                self._pause_game()
            elif self.stats.game_pause:
                self._resume_game()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_end_button(self, mouse_pos):
        """
        Go to the first menu when the player
        won the game and clicks the screen
        """
        end_clicked = self.won_button.b_rect.collidepoint(mouse_pos)
        if end_clicked:
            # Play sound of clicked buttom.
            self.click_sound.play()
            return "restart"

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        play_clicked = self.play_button.b_rect.collidepoint(mouse_pos)
        if play_clicked:
            # Play sound of clicked buttom.
            self.click_sound.play()
            self._start_game()

    def _check_pause_buttons(self, mouse_pos):
        """Resume the game when the player clicks Resume"""
        resume_clicked = self.resume_button.b_rect.collidepoint(mouse_pos)
        quit_clicked = self.quit_button.b_rect.collidepoint(mouse_pos)

        # If user is anonymous, don't offer save option.
        if self.user != "anon":
            save_clicked = self.save_button.b_rect.collidepoint(mouse_pos)
        else:
            save_clicked = None

        if resume_clicked:
            self._resume_game()
        elif save_clicked:
            return self._save_game()
        elif quit_clicked:
            # Play sound of clicked buttom.
            self.click_sound.play()
            return self._exit_game()

    ########################################################################################
    # Start-stop game functions
    ########################################################################################

    def _start_game(self):
        """Starts a new game"""

        # Play ambient sound for the game.
        self.ambient_sound.play(loops=-1, fade_ms=500)

        if not self.saved_game:

            # Reset the game statistics.
            self.stats.reset_stats()

            # Reset the game settings.
            self.settings.initialize_dynamic_settings(self.ini_diff)

            # Set scoring images.
            self.sb.prep_images()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

        # Starts game.
        self.stats.game_active = True

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _resume_game(self):
        """Resume game after being paused"""
        self.stats.game_pause = False

        # Play sound of clicked buttom.
        self.click_sound.play()

        # Restart ambient sound.
        self.ambient_sound.play(loops=-1, fade_ms=500)

    def _save_game(self):
        """Save game state"""

        # Play sound of clicked buttom.
        self.click_sound.play()

        # Construct key.
        date = datetime.now().strftime("%Y-%m-%d, %H:%M")
        key = f"{self.user}({date})"

        # Save game.
        saved_game = self._get_current_game_data()

        # Store saved game.
        try:
            with open(self.saved_games_filename) as f:
                saved_games = json.load(f)
        except FileNotFoundError:
            saved_games = {}
        saved_games[key] = saved_game

        # Sort the whole list of saved games by user first, and then date.
        with open(self.saved_games_filename, "w") as f:
            sorted_saved_games = {
                k: v
                for k, v in sorted(
                    saved_games.items(),
                    key=lambda item: (item[1]["user"], item[1]["date"]),
                )
            }
            json.dump(sorted_saved_games, f)

        # Quit game.
        return self._exit_game()

    def _get_current_game_data(self):
        """Get all the data that defines the current state of the game"""
        aliens_data = []
        for alien in self.aliens.sprites():
            alien_data = {
                "x": alien.x,
                "y": alien.rect.y,
            }
            aliens_data.append(alien_data)

        saved_game = {
            # Scores.
            "high_score": self.stats.high_score,
            "ship_left": self.stats.ships_left,
            "current_score": self.stats.score,
            "level": self.stats.level,
            # Configuration.
            "user": self.user,
            "ini_diff": self.ini_diff,
            "screen_size": self.screen_size,
            # Speeds.
            "ship_speed": self.settings.ship_speed,
            "bullet_speed": self.settings.bullet_speed,
            "alien_speed": self.settings.alien_speed,
            "alien_points": self.settings.alien_points,
            "fleet_direction": self.settings.fleet_direction,
            # Screen state.
            "ship_x": self.ship.x,
            "aliens": aliens_data,
            # Date (used to sort the saved games by user and date).
            "date": float(datetime.now().timestamp() * 1000),
        }

        return saved_game

    def _exit_game(self):
        """Store highest score and exit game"""

        # Stop ambient sound.
        self.ambient_sound.fadeout(500)

        pygame.mouse.set_visible(True)

        self.stats.game_active = False
        self.stats.game_end = False

        if self.user != "anon":
            with open(self.high_scores_filename) as f:
                user_scores = json.load(f)
            past_high_score = user_scores[self.user]["high_score"]

            if self.stats.score >= past_high_score:
                user_scores[self.user]["high_score"] = self.stats.high_score
                user_scores[self.user]["lives_left"] = self.stats.ships_left + 1
                user_scores[self.user]["max_level"] = self.stats.level
                user_scores[self.user]["date"] = datetime.now().strftime(
                    "%Y-%m-%d, %H:%M:%S"
                )

            with open(self.high_scores_filename, "w") as f:
                json.dump(user_scores, f)

        return "restart"

    def _pause_game(self):
        """Pause game"""

        # Stop ambient sound.
        self.ambient_sound.fadeout(500)

        self.stats.game_pause = True
        pygame.mouse.set_visible(True)

    def _show_won_game_message(self):
        """Show a message once the game is won"""

        # Stop ambient sound.
        self.ambient_sound.fadeout(500)

        self.won_button.draw_button(self.screen)
        pygame.display.flip()
        pygame.mouse.set_visible(True)
        self.game_won_sound.play()
        self.stats.game_active = False
        self.stats.game_end = True

    ########################################################################################
    # Game logic and actions functions
    ########################################################################################

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            # Play sound of firing a bullet.
            self.laser_sound.play()
        else:
            # Play sound of misfired bullet.
            self.fail_shot.play()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""

        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # If a collision occurred, update scores.
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # If there are no more aliens start a new level.
        if not self.aliens:
            self._start_new_level()

    def _start_new_level(self):
        """Go to next level"""

        # Destroy existing bullets, create new fleet and increase speed.
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        # Increase level.
        self.stats.level += 1
        self.sb.prep_level()

    def _update_aliens(self):
        """
        Check if the fleet is at an edge, update the positions of all aliens in the fleet
        and check for alien collisions.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""

        # Play sound of losing a ship.
        self.loose_ship_sound.play()

        # Stop ambient sound.
        self.ambient_sound.fadeout(500)

        if self.stats.ships_left > 0:
            self._next_ship()
        else:
            self.stats.game_active = False
            # Pause.
            sleep(0.8)
            # Show that the last ship was lost.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            pygame.mouse.set_visible(True)

    def _next_ship(self):
        """Restart game after losing one ship"""

        # Decrement ships_left.
        self.stats.ships_left -= 1
        self.sb.prep_ships()

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Pause.
        sleep(0.8)

        # Restart ambient sound.
        self.ambient_sound.play(loops=-1, fade_ms=500)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break


############################################################################################
# Main
############################################################################################

if __name__ == "__main__":

    if getattr(sys, "frozen", False):

        main_path = ""
        os.chdir(os.path.dirname(sys.executable))

        # Create `user_data` folder if it does not exist.
        if not os.path.exists('user_data'):
            os.makedirs('user_data')

    else:

        main_path = "src/"

        # Create `src/user_data` folder if it does not exist.
        if not os.path.exists('src/user_data'):
            os.makedirs('src/user_data')

    while True:

        configuration = conff_menu(main_path)

        # Make a game instance, and run the game.
        ai = AlienInvasion(configuration, main_path)
        ai.run_game()
