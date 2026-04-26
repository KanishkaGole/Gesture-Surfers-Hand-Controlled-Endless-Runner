import pygame
import random
import math
from utils.constants import *

class Entity:
    def __init__(self, lane, y, speed):
        self.lane = lane
        self.x = LANES[lane]
        self.y = y
        self.speed = speed
        self.width = 60
        self.height = 60
        self.rect = pygame.Rect(self.x - self.width//2, self.y, self.width, self.height)

    def update(self, speed):
        self.speed = speed
        self.y += self.speed
        self.rect.y = self.y

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT

class Obstacle(Entity):
    TYPES = ["BLOCK", "JUMP", "SLIDE", "DRONE"]

    def __init__(self, speed, type=None, lane=None):
        lane = random.randint(0, 2) if lane is None else lane
        # All obstacles now start well above the screen for better reaction time
        super().__init__(lane, -300, speed)
        
        self.type = random.choice(self.TYPES) if type is None else type
        self.pulse = 0
        
        if self.type == "BLOCK":
            self.height = 120
            self.color = OBSTACLE_BLOCK_COLOR
        elif self.type == "JUMP":
            self.height = 40
            self.color = OBSTACLE_JUMP_COLOR
            # Jump obstacles are on the ground (visually we offset them later if needed)
        elif self.type == "SLIDE":
            self.height = 180
            self.color = OBSTACLE_SLIDE_COLOR
        elif self.type == "DRONE":
            self.height = 50
            self.width = 80
            self.color = (255, 165, 0)
            self.move_dir = 1
            self.initial_x = self.x

        self.rect = pygame.Rect(self.x - self.width//2, self.y, self.width, self.height)

    def update(self, speed):
        super().update(speed)
        self.pulse += 0.1
        if self.type == "DRONE":
            offset = math.sin(self.pulse) * 40
            self.rect.x = self.initial_x - self.width//2 + offset

    def draw(self, screen):
        # We draw based on their logical "y" but offset certain types for visual perspective
        draw_y = self.y
        
        # Adjust visual position for JUMP (low) vs SLIDE (high) to make it intuitive
        # In a 2D top-down-ish view, JUMP is usually a bar on the floor.
        # SLIDE is a bar in the air.
        
        if self.type == "BLOCK":
            pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=8)
        elif self.type == "JUMP":
            # Jump obstacles: Draw a ground-level barrier
            # We use the rect as is, but maybe draw it slightly differently
            pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=5)
        elif self.type == "SLIDE":
            # Slide obstacles: Draw as an overhead beam
            # The player must slide under this.
            pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
            # Add "danger" stripes to show it's high
            for i in range(0, self.rect.height, 20):
                pygame.draw.line(screen, (0,0,0), (self.rect.left, self.rect.top + i), (self.rect.right, self.rect.top + i + 10), 2)
        elif self.type == "DRONE":
            pygame.draw.ellipse(screen, self.color, self.rect)
            pygame.draw.circle(screen, (255, 255, 255), self.rect.center, 10)

class Coin(Entity):
    def __init__(self, lane, y, speed):
        super().__init__(lane, y, speed)
        self.width = 30
        self.height = 30
        self.angle = 0
        self.rect = pygame.Rect(self.x - self.width//2, self.y, self.width, self.height)

    def update(self, speed):
        super().update(speed)
        self.angle += 0.1

    def draw(self, screen):
        rot_width = abs(math.cos(self.angle)) * self.width
        coin_rect = pygame.Rect(self.x - rot_width//2, self.y, rot_width, self.height)
        pygame.draw.ellipse(screen, COIN_COLOR, coin_rect)
        pygame.draw.ellipse(screen, (255, 255, 255), coin_rect, 2)
