import pygame
from constants import *

class Scoreboard:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def draw(self, level_number, score, cannonballs_left):
        """Display the scoreboard."""

        # Level
        level_text = self.font.render(f"Level: {level_number}", True, "Black")
        level_text_rect = level_text.get_rect(topleft=(10, 10))
        self.screen.blit(level_text, level_text_rect)

        # Score
        score_text = self.font.render(f"Score: {score}", True, "Black")
        score_text_rect = score_text.get_rect(topleft=(10, 50))
        self.screen.blit(score_text, score_text_rect)

        # Cannonballs left
        cannonballs_left_text = self.font.render(
            f"Cannonballs Left: {cannonballs_left}",
            True,
            "Black"
        )
        cannonballs_left_text_rect = cannonballs_left_text.get_rect(topleft=(10, 90))
        self.screen.blit(cannonballs_left_text, cannonballs_left_text_rect)