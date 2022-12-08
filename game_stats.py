# class GameStats:
#     def __init__(self, ai_game):
#         self.settings = ai_game.settings
#         self.reset_stats()
#
#         self.game_active = True
#
#     def reset_stats(self):
#         self.ships_left = self.settings.ship_limit

class GameStats:
    """Track statistics for the game."""

    def __init__(self, ss_game):
        """Initialize statistics."""
        self.settings = ss_game.settings
        self.reset_stats()

        # Start game in an active state.
        self.game_active = True

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.cars_left = self.settings.car_limit