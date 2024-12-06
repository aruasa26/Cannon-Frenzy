""" This module initializes and manages the game. """

import sys
import pygame
import sprites
from constants import *
from level import Level
from levels_config import LEVELS_CONFIG
from menu import Menu
from scoreboard import Scoreboard
from sound_manager import SoundManager


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

        # Level configurations
        self.levels = [Level(self.screen, **config) for config in LEVELS_CONFIG]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]

        # Scoreboard
        self.scoreboard = Scoreboard(self.screen)

        # Sound manager
        self.sound_manager = SoundManager()
        self.game_over_sound_played = False

        # Menu manager
        self.menu = Menu(self.screen, self.sound_manager)

        # Background Image
        self.level_bg_image = pygame.image.load("assets/images/backgrounds/grasslands.png")

        # Initial properties -> Level 1
        self.score = 0
        self.game_over = False
        self.cannonballs = []
        self.cannon = sprites.Cannon(
            self.screen,
            self.cannonballs,
            self.current_level.cannonballs_left
        )

        # Combo tracker
        self.combo_count = 0
        self.max_combo_streak = 0

<<<<<<< HEAD
        self.game_over_sound = pygame.mixer.Sound("assets/audio/mixkit-funny-game-over-2878.wav")
        self.game_over_sound.set_volume(0.9)
        self.game_over_sound_played = False

        self.target_hit_sound = pygame.mixer.Sound("assets/audio/sfx/target_hit.ogg")
        self.target_hit_sound.set_volume(0.7)

        #Level Transition sound
        self.level_entry_sound = pygame.mixer.Sound("assets/audio/mixkit-game-level-completed-2059.wav")
        self.level_entry_sound.set_volume(0.5)

        #Gameplay Background Music
        self.background_music = "assets/audio/mixkit-deep-urban-623.mp3"
        pygame.mixer.music.set_volume(0.3)

        # Game started flag
        self.game_started = False

    def start_menu(self):
        """Displays the start menu."""

        # Load and play background music
        pygame.mixer.music.load("assets/audio/mixkit-games-music-706.mp3")
        pygame.mixer.music.play(-1)

        while not self.game_started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.game_started = True
                        pygame.mixer.music.stop()
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
=======
>>>>>>> 69d4fcdf6656fb5a93a67570b0f27eb8ca0d17eb

    def reset_game(self):
        """Resets the game state."""
        self.game_over_sound_played = False
        self.levels = [Level(self.screen, **config) for config in LEVELS_CONFIG]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]
        self.score = 0
        self.game_over = False
        self.cannonballs = []
        self.cannon = sprites.Cannon(self.screen, self.cannonballs, self.current_level.cannonballs_left)
        self.combo_count = 0
        self.max_combo_streak = 0


    def run(self):
        """Runs the game."""

        # Start menu
        self.menu.start_menu()

<<<<<<< HEAD
        # Flag for tracking background music
        background_music_playing = False

=======
        # Game loop
>>>>>>> 69d4fcdf6656fb5a93a67570b0f27eb8ca0d17eb
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and self.game_over:
                    # Press 'R' key to restart the game
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.sound_manager.game_start_sound.play()

                    # Press 'M' key to go back to the start menu
                    if event.key == pygame.K_m:
                        self.reset_game()
                        self.menu.start_menu()

            # Game over condition
            if self.cannon.cannonballs_left == 0 and len(self.cannon.cannonballs) == 0:
                self.game_over = True

            if self.game_over:
                self.handle_game_over()
                background_music_playing = False  # Stop background music on game over
                pygame.mixer.music.stop()
            else:
                # Play background music if not already playing
                if not background_music_playing:
                    pygame.mixer.music.load(self.background_music)
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                    background_music_playing = True

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
                        self.combo_count = 0

                    for target in self.current_level.targets[:]:
                        if target.hit(cannonball):
                            self.sound_manager.target_hit_sound.play()
                            self.current_level.targets.remove(target)
                            self.cannonballs.remove(cannonball)
                            self.combo_count += 1
                            if self.combo_count > self.max_combo_streak:
                                self.max_combo_streak = self.combo_count
                            self.score += 10 + 5 * (self.combo_count - 1)
                            break

                # Check if all targets are hit
                if not self.current_level.targets:
                    self.current_level_index += 1
                    if self.current_level_index < len(self.levels):
                        self.level_entry_sound.play()
                        self.current_level = self.levels[self.current_level_index]
                        cannonballs_left = self.current_level.cannonballs_left
                        self.cannon = sprites.Cannon(self.screen, self.cannonballs, cannonballs_left)

<<<<<<< HEAD
                    else:
                        self.game_over = True

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
=======
                # Display the scoreboard
                self.scoreboard.draw(
                    level_number=self.current_level.level_number,
                    score=self.score,
                    combo_count=self.combo_count,
                    max_combo_streak=self.max_combo_streak,
                    cannonballs_left=self.cannon.cannonballs_left
>>>>>>> 69d4fcdf6656fb5a93a67570b0f27eb8ca0d17eb
                )

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
            self.sound_manager.game_over_sound.play()

        # Draw the game over screen
        self.menu.game_over_menu(self.score)
