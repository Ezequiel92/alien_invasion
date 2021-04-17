class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self, ini_diff):
        """Initialize the game's static settings"""

        # Small screen settings.
        self.screen_width = 800
        self.screen_height = 705

        # Background color.
        self.bg_color = (230, 230, 230)

        # Extra ships (initial lives = extra ships + 1).
        self.ship_limit = 2

        # Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings.
        self.fleet_drop_speed = 10

        # How quickly the game speeds up.
        self.speedup_scale = 1.03
        # How quickly the alien point values increase.
        self.score_scale = 1.2
        # Set initial difficulty.
        self.initialize_dynamic_settings(ini_diff)

    def initialize_dynamic_settings(self, ini_diff):
        """Initialize settings that change throughout the game"""

        # Set initial difficulty.
        self.alien_speed = ini_diff[0]
        self.bullet_speed = ini_diff[1]
        self.ship_speed = ini_diff[2]

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # How many points killing an alien gives.
        self.alien_points = 20

    def increase_speed(self):
        """Increase speed settings and alien point values"""

        # Max. ship speed = 4.
        if self.ship_speed <= 4:
            self.ship_speed *= self.speedup_scale

        # Max. bullet speed = 8.
        if self.bullet_speed <= 8:
            self.bullet_speed *= self.speedup_scale

        # Max. bullet speed = 8.
        if self.alien_speed <= 3:
            self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
