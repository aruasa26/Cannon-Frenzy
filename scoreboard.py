import pygame
from constants import *

class Scoreboard:
    def __init__(self, screen):
        self.screen = screen
        self.x = 10
        self.y = 10
        self.font = pygame.font.Font(None, 32)

    def draw(self, level_number, score, combo_count, max_combo_streak, cannonballs_left):
        """Display the scoreboard."""

        # Level
        level_text = self.font.render(f"Level: {level_number}", True, "Black")
        level_text_rect = level_text.get_rect(topleft=(self.x, self.y))
        self.screen.blit(level_text, level_text_rect)

        # Score
        score_text = self.font.render(f"Score: {score}", True, "Black")
        score_text_rect = score_text.get_rect(topleft=(self.x, self.y + 30))
        self.screen.blit(score_text, score_text_rect)

        # Combo count
        combo_count_text = self.font.render(f"Combo count: {combo_count}", True, "Black")
        combo_count_text_rect = combo_count_text.get_rect(topleft=(self.x, self.y + 60))
        self.screen.blit(combo_count_text, combo_count_text_rect)

        # Max combo count
        max_combo_count_text = self.font.render(f"Max combo count: {max_combo_streak}", True, "Black")
        max_combo_count_text_rect = max_combo_count_text.get_rect(topleft=(self.x, self.y + 90))
        self.screen.blit(max_combo_count_text, max_combo_count_text_rect)

        # Cannonballs left
        cannonballs_left_text = self.font.render(
            f"Cannonballs Left: {cannonballs_left}",
            True,
            "Black"
        )
        cannonballs_left_text_rect = cannonballs_left_text.get_rect(topright=(SCREEN_WIDTH - self.x, self.y))
        self.screen.blit(cannonballs_left_text, cannonballs_left_text_rect)