""" This module initializes and manages the game. """

import sys
import pygame
import sprites
from constants import *
from level import Level
from levels_config import LEVELS_CONFIG


class CannonFrenzy:
    def __init__(self):
        # Initialize pygame modules
        pygame.init()

        # Stop the game if pygame fails to initialize
        if not pygame.get_init():
            print("Failed to initialize Pygame!")
            sys.exit()

        # Set game properties
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cannon Frenzy")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 36)

        # Levels configuration
        self.levels = [Level(self.screen, **config) for config in LEVELS_CONFIG]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]

        # Background Image
        self.level_bg_image = pygame.image.load("assets/images/backgrounds/grasslands.png")
        self.menu_bg_image = pygame.image.load("assets/images/backgrounds/clouds.jpg")
        self.menu_bg_image = pygame.transform.scale(self.menu_bg_image, (800, 600))

        # Initial properties -> Level 1
        self.score = 0
        self.game_over = False
        self.cannonballs = []
        self.cannon = sprites.Cannon(
            self.screen,
            self.cannonballs,
            self.current_level.cannonballs_left
        )

        # Sounds
        self.game_start_sound = pygame.mixer.Sound("assets/audio/sfx/game_start.wav")
        self.game_start_sound.set_volume(0.5)

        self.game_over_sound = pygame.mixer.Sound("assets/audio/sfx/game_over.wav")
        self.game_over_sound.set_volume(0.5)
        self.game_over_sound_played = False

        self.target_hit_sound = pygame.mixer.Sound("assets/audio/sfx/target_hit.ogg")
        self.target_hit_sound.set_volume(0.5)

        # Background music
        self.start_menu_music = pygame.mixer.Sound("assets/audio/music/action_modern_reels.mp3")
        self.start_menu_music.set_volume(0.5)

        # Game started flag
        self.game_started = False

    def start_menu(self):
        """Displays the start menu."""
        self.start_menu_music.play(loops=-1)

        while not self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.game_started = True
                        self.start_menu_music.stop()
                        self.game_start_sound.play()

            # Draw menu background
            self.screen.blit(self.menu_bg_image, (0, 0))

            # Display game title
            title_text = self.font.render("Cannon Frenzy", True, "Black")
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            self.screen.blit(title_text, title_rect)

            # Display start instructions
            start_text = self.small_font.render("Press S to Start", True, "Black")
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(start_text, start_rect)

            pygame.display.update()
            self.clock.tick(self.fps)

    def reset_game(self):
        """Resets the game state."""
        self.levels = [Level(self.screen, **config) for config in LEVELS_CONFIG]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]
        self.score = 0
        self.game_over = False
        self.cannonballs = []
        self.cannon = sprites.Cannon(self.screen, self.cannonballs, self.current_level.cannonballs_left)

    def run(self):
        """Runs the game loop."""
        # Start menu
        self.start_menu()

        # Game start sound
        self.game_start_sound.play()

        while self.game_started:
            # Event handling
            for event in pygame.event.get():
                # On exiting the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and self.game_over:
                    # Press 'R' key to restart the game
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.game_over_sound_played = False
                        self.game_start_sound.play()

                    # Press 'M' key to go back to the start menu
                    if event.key == pygame.K_m:
                        self.game_started = False
                        self.reset_game()
                        self.start_menu()

            # Game over condition
            if self.cannon.cannonballs_left == 0 and len(self.cannon.cannonballs) == 0:
                self.game_over = True

            if self.game_over:
                self.handle_game_over()
            else:
                # Determine background image according to level number
                if self.current_level.level_number % 2 == 0:
                    self.level_bg_image = pygame.image.load("assets/images/backgrounds/desert.png")
                else:
                    self.level_bg_image = pygame.image.load("assets/images/backgrounds/grasslands.png")

                self.screen.blit(self.level_bg_image, (0, 0))
                self.cannon.draw()
                self.current_level.draw()

                for cannonball in self.cannonballs[:]:
                    cannonball.move()
                    cannonball.draw()

                    if cannonball.is_off_screen():
                        self.cannonballs.remove(cannonball)

                    for target in self.current_level.targets[:]:
                        if target.hit(cannonball):
                            self.target_hit_sound.play()
                            self.current_level.targets.remove(target)
                            self.cannonballs.remove(cannonball)
                            self.score += 10
                            break

                # Check if all targets are hit
                if not self.current_level.targets:
                    self.current_level_index += 1
                    if self.current_level_index < len(self.levels):
                        self.current_level = self.levels[self.current_level_index]
                        cannonballs_left = self.current_level.cannonballs_left
                        self.cannon = sprites.Cannon(self.screen, self.cannonballs, cannonballs_left)

                # Display level, score, and cannonballs left
                self.font = pygame.font.Font(None, 36)

                level_text = self.font.render(f"Level: {self.current_level.level_number}", True, "Black")
                level_text_rect = level_text.get_rect(topleft=(10, 10))
                self.screen.blit(level_text, level_text_rect)

                score_text = self.font.render(f"Score: {self.score}", True, "Black")
                score_text_rect = score_text.get_rect(topleft=(10, 50))
                self.screen.blit(score_text, score_text_rect)

                cannonballs_left_text = self.font.render(
                    f"Cannonballs Left: {self.cannon.cannonballs_left}",
                    True,
                    "Black"
                )
                cannonballs_left_text_rect = cannonballs_left_text.get_rect(topleft=(10, 90))
                self.screen.blit(cannonballs_left_text, cannonballs_left_text_rect)

                # Update the cannon sprite
                self.cannon.update()

            pygame.display.update()
            self.clock.tick(self.fps)

    def handle_game_over(self):
        """Displays the game over screen."""
        pygame.display.update()
        self.clock.tick(self.fps)
        pygame.time.delay(1000)

        # Game over sound
        if not self.game_over_sound_played:
            self.game_over_sound_played = True
            self.game_over_sound.play()

        # Game over screen
        sunset_image = pygame.image.load("assets/images/backgrounds/sunset_pixel.jpg")
        self.screen.blit(sunset_image, (0, 0))
        self.font = pygame.font.Font(None, 50)
        game_over_text = self.font.render("GAME OVER!", True, "Black")
        game_over_rect = game_over_text.get_rect(center=(400, 200))
        self.screen.blit(game_over_text, game_over_rect)

        score_text = self.font.render(f"Score: {self.score}", True, "Black")
        score_text_rect = score_text.get_rect(center=(400, 300))
        self.screen.blit(score_text, score_text_rect)

        restart_text = self.font.render("R - Restart Game", True, "Black")
        restart_text_rect = restart_text.get_rect(center=(400, 360))
        self.screen.blit(restart_text, restart_text_rect)

        start_menu_text = self.font.render("M - Start Menu", True, "Black")
        start_menu_text_rect = restart_text.get_rect(center=(400, 420))
        self.screen.blit(start_menu_text, start_menu_text_rect)
