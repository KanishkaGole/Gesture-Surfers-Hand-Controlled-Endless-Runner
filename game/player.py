import pygame
from utils.constants import *

class Player:
    def __init__(self):
        self.lane = CENTER_LANE
        self.x = LANES[self.lane]
        self.y = SCREEN_HEIGHT - 100
        self.width = 50
        self.height = 80
        
        self.is_jumping = False
        self.jump_vel = 0
        
        self.is_sliding = False
        self.slide_timer = 0
        
        self.rect = pygame.Rect(self.x - self.width//2, self.y - self.height, self.width, self.height)

    def update(self):
        # Update horizontal position (smooth transition)
        target_x = LANES[self.lane]
        self.x += (target_x - self.x) * 0.2
        
        # Jump logic
        if self.is_jumping:
            self.y += self.jump_vel
            self.jump_vel += GRAVITY
            if self.y >= SCREEN_HEIGHT - 100:
                self.y = SCREEN_HEIGHT - 100
                self.is_jumping = False
                self.jump_vel = 0
        
        # Slide logic
        if self.is_sliding:
            self.slide_timer -= 1
            if self.slide_timer <= 0:
                self.is_sliding = False
                self.height = 80
        
        # Update rect for collisions
        current_height = 40 if self.is_sliding else 80
        self.rect = pygame.Rect(self.x - self.width//2, self.y - current_height, self.width, current_height)

    def move_left(self):
        if self.lane > LEFT_LANE:
            self.lane -= 1

    def move_right(self):
        if self.lane < RIGHT_LANE:
            self.lane += 1

    def set_lane(self, lane_index):
        if LEFT_LANE <= lane_index <= RIGHT_LANE:
            self.lane = lane_index

    def jump(self):
        if not self.is_jumping and not self.is_sliding:
            self.is_jumping = True
            self.jump_vel = JUMP_HEIGHT

    def slide(self):
        if not self.is_jumping and not self.is_sliding:
            self.is_sliding = True
            self.slide_timer = SLIDE_DURATION
            self.height = 40

    def draw(self, screen):
        color = PLAYER_COLOR
        # Draw multi-layered glow
        for i in range(4, 0, -1):
            alpha = 100 // i
            glow_rect = self.rect.inflate(i*4, i*4)
            s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(s, (*color, alpha), (0, 0, glow_rect.width, glow_rect.height), border_radius=12)
            screen.blit(s, glow_rect.topleft)
            
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=10)
