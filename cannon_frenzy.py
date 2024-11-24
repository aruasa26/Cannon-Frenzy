""" This module initializes and manages the game. """

import random
import sys
import pygame
import sprites
from constants import *


class CannonFrenzy:
    def __init__(self):
        # Initialize pygame modules
        pygame.init()

        # Set game properties
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cannon Frenzy")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.SysFont(None, 20)

    def run(self):
        """ Runs the game loop. """
        cannonballs = []
        cannonballs_left = 7

        cannon = sprites.Cannon(self.screen, cannonballs, cannonballs_left)
        targets = [
            sprites.Target(
                screen = self.screen,
                x = random.randint(400, SCREEN_WIDTH - 50),
                y = random.randint(200, 400),
                width = 50,
                height = 50
            )
            for _ in range(5)
        ]

        score = 0
        game_over = False

        while True:

            # Event handling
            for event in pygame.event.get():

                # On exiting the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Game over condition
            if cannon.cannonballs_left == 0 and len(cannon.cannonballs) == 0:
                game_over = True

            if not game_over:
                self.screen.fill("White")
                cannon.draw()
                for target in targets:
                    target.draw()

                for cannonball in cannonballs[:]:
                    cannonball.move()
                    cannonball.draw()

                    if cannonball.is_off_screen():
                        cannonballs.remove(cannonball)

                    for target in targets[:]:
                        if target.hit(cannonball):
                            targets.remove(target)
                            cannonballs.remove(cannonball)
                            score += 10
                            break

                # Display score and cannonballs left
                font = pygame.font.SysFont(None, 36)
                score_text = font.render(f"Score: {score}", True, "Black")
                self.screen.blit(score_text, (10, 10))

                cannonballs_left_text = font.render(
                    f"Cannonballs Left: {cannon.cannonballs_left}",
                    True,
                    "Black"
                )
                self.screen.blit(cannonballs_left_text, (10, 50))

                # Update the cannon sprite
                cannon.update()

            # On game over
            else:
                pygame.display.update()
                self.clock.tick(self.fps)
                pygame.time.delay(1000)

                # Game over screen
                self.screen.fill("White")
                font = pygame.font.SysFont(None, 36)
                game_over_text = font.render("GAME OVER", True, "Black")
                game_over_rect = game_over_text.get_rect(center=(400, 160))
                self.screen.blit(game_over_text, game_over_rect)

                score_text = font.render(f"Score: {score}", True, "Black")
                score_text_rect = score_text.get_rect(center=(400, 200))
                self.screen.blit(score_text, score_text_rect)

                cannonballs_left_text = font.render(
                    f"Cannonballs Left: {cannonballs_left}",
                    True,
                    "Black"
                )
                cannonballs_left_rect = cannonballs_left_text.get_rect(center=(400, 240))
                self.screen.blit(cannonballs_left_text, cannonballs_left_rect)

            pygame.display.update()
            self.clock.tick(self.fps)


