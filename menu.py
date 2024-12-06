import sys
import pygame

from constants import *
from sound_manager import SoundManager


class Menu:
    def __init__(self, screen, sound_manager: SoundManager):
        self.screen = screen
        self.sound_manager = sound_manager

        # Fonts
        self.font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 36)

        # Background images
        self.start_menu_bg_image = pygame.image.load("assets/images/backgrounds/clouds.jpg")
        self.start_menu_bg_image = pygame.transform.scale(self.start_menu_bg_image, (800, 600))

        self.game_over_menu_bg_image = pygame.image.load("assets/images/backgrounds/night_sky.jpg")
        self.game_over_menu_bg_image = pygame.transform.scale(self.game_over_menu_bg_image, (800, 600))


    def start_menu(self):
        """Displays the game's start menu."""
        self.sound_manager.start_menu_music.play(loops=-1)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.sound_manager.start_menu_music.stop()
                    self.sound_manager.game_start_sound.play()
                    return

            # Draw menu background
            self.screen.blit(self.start_menu_bg_image, (0, 0))

            # Display game title
            title_text = self.font.render("Cannon Frenzy", True, "Black")
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            self.screen.blit(title_text, title_rect)

            # Display start instructions
            start_text = self.small_font.render("Press S to Start", True, "Black")
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(start_text, start_rect)

            pygame.display.update()

    def game_over_menu(self, score):
        """Displays the Game over screen"""
        self.screen.blit(self.game_over_menu_bg_image, (0, 0))
        font = pygame.font.Font(None, 50)
        game_over_text = font.render("GAME OVER", True, "White")
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)

        score_text = font.render(f"Score: {score}", True, "White")
        score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 260))
        self.screen.blit(score_text, score_text_rect)

        restart_text = font.render("R - Restart Game", True, "White")
        restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 360))
        self.screen.blit(restart_text, restart_text_rect)

        start_menu_text = font.render("M - Start Menu", True, "White")
        start_menu_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 420))
        self.screen.blit(start_menu_text, start_menu_text_rect)

        pygame.display.update()

