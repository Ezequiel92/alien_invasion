class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game, high_score):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start game in an inactive state and not paused.
        self.game_active = False
        self.game_pause = False
        self.game_end = False

        # High score.
        self.high_score = high_score

    def reset_stats(self):
        """Initialize statistics which are reset with a new game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
