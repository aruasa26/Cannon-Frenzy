""" This module contains the sprites used throughout the game. """

import pygame
import math
from constants import *

class Cannon(pygame.sprite.Sprite):
    def __init__(self, screen, cannonballs, cannonballs_left, power=25):
        super().__init__()
        self.screen = screen
        self.cannonballs = cannonballs
        self.cannonballs_left = cannonballs_left
        self.power = power
        self.x = 100
        self.y = SCREEN_HEIGHT - 60
        self.angle = 45

        # Cannon fire sound
        self.cannon_fire_sound = pygame.mixer.Sound("assets/audio/sfx/cannon_fire.ogg")
        self.cannon_fire_sound.set_volume(0.5)

    def draw(self):
        # Cannon base
        pygame.draw.rect(self.screen, "Black", (self.x - 10, self.y - 30, 20, 30))

        # Cannon barrel
        cannon_length = 50
        end_x = self.x + cannon_length * math.cos(math.radians(self.angle))
        end_y = self.y - cannon_length * math.sin(math.radians(self.angle))
        pygame.draw.line(self.screen, "Red", (self.x, self.y), (end_x, end_y), 5)

    def adjust_angle(self, change):
        """ Adjusts the cannon barrel's angle.
        :param change: Angle to adjust.
        """
        self.angle = max(10, min(80, self.angle + change))  # Restrict angle between 10° and 80°

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.adjust_angle(-1)
        if keys[pygame.K_DOWN]:
            self.adjust_angle(1)
        if keys[pygame.K_SPACE] and len(self.cannonballs) == 0 and self.cannonballs_left > 0:
            self.cannon_fire_sound.play()
            self.cannonballs.append(Cannonball(self.screen, self.x, self.y, self.angle, self.power))
            self.cannonballs_left -= 1

    def update(self):
        self.move()


class Cannonball(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, angle, power):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = 8
        self.speed_x = power * math.cos(math.radians(angle))
        self.speed_y = -power * math.sin(math.radians(angle))
        self.gravity = 0.5  # Gravity effect

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += self.gravity  # Simulate gravity

    def draw(self):
        pygame.draw.circle(self.screen, "Black", (int(self.x), int(self.y)), self.radius)

    def is_off_screen(self):
        """ Checks if the cannonball is off-screen. """
        return self.x > SCREEN_WIDTH or self.y > SCREEN_HEIGHT


class Target(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, width, height, color="Blue"):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def hit(self, cannonball):
        """ Checks if the target has been hit by a cannonball.
        :param cannonball: Cannonball to check.
        """
        return (
            self.x < cannonball.x < self.x + self.width and
            self.y < cannonball.y < self.y + self.height
        )