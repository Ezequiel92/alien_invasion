import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """A class to report scoring information"""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes"""

        # Load game assets and data.
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.scree_rect = self.ai_game.screen_rect
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font_filename = ai_game.path + "fonts/unispace.ttf"
        self.font = pygame.font.Font(self.font_filename, 30)

        # Prepare the initial score images.
        self.prep_images()

    ################################################################################################
    # Functions to construct scoring images on the screen
    ################################################################################################

    def prep_images(self):
        """Prepare the initial score images."""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image"""

        # Render the current score.
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.scree_rect.right - 20
        self.score_rect.top = 15

    def prep_high_score(self):
        """Turn the high score into a rendered image"""

        # Render the high score.
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color
        )

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.scree_rect.centerx
        self.high_score_rect.top = self.score_rect.top - 5

    def prep_level(self):
        """Turn the level into a rendered image"""

        # Render the current level.
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color
        )

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left + 1):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    ################################################################################################
    # Auxiliary functions
    ################################################################################################

    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.high_score:
            # Updates high score on stats.
            self.stats.high_score = self.stats.score
            # Updates high score on screen.
            self.prep_high_score()

    def show_score(self):
        """Draw scores, level, and ships to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
