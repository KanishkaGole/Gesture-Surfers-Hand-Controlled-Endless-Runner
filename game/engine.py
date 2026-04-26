import pygame
import random
from utils.constants import *
from game.player import Player
from game.obstacle import Obstacle, Coin
from vision.hand_tracker import HandTracker

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Gesture Surfers - Ultra Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 32, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 18)
        
        self.hand_tracker = HandTracker()
        self.reset()

    def reset(self):
        self.player = Player()
        self.obstacles = []
        self.coins = []
        self.speed = INITIAL_SPEED
        self.score = 0
        self.coin_score = 0
        self.game_over = False
        self.spawn_timer = 0
        self.pattern_cooldown = 0

    def run(self):
        self.hand_tracker.start()
        
        running = True
        while running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset()
                    if event.key == pygame.K_ESCAPE:
                        running = False

            if not self.game_over:
                self._handle_gestures()
                self._update()
            
            self._draw()
            
        self.hand_tracker.stop()
        pygame.quit()

    def _handle_gestures(self):
        gesture = self.hand_tracker.get_gesture()
        if gesture == "LANE_0":
            self.player.set_lane(LEFT_LANE)
        elif gesture == "LANE_1":
            self.player.set_lane(CENTER_LANE)
        elif gesture == "LANE_2":
            self.player.set_lane(RIGHT_LANE)
        elif gesture == "JUMP":
            self.player.jump()
        elif gesture == "SLIDE":
            self.player.slide()

    def _update(self):
        self.speed += SPEED_INCREMENT
        self.score += 1
        
        self.player.update()
        
        # Spawning Logic (Pattern Based)
        self.spawn_timer += 1
        if self.spawn_timer > max(20, 60 - int(self.speed)):
            self._spawn_pattern()
            self.spawn_timer = 0
            
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.update(self.speed)
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
            elif self.player.rect.colliderect(obstacle.rect):
                # Specific check for mechanics
                if obstacle.type == "JUMP" and self.player.is_jumping:
                    continue
                if obstacle.type == "SLIDE" and self.player.is_sliding:
                    continue
                self.game_over = True
                
        # Update coins
        for coin in self.coins[:]:
            coin.update(self.speed)
            if coin.is_off_screen():
                self.coins.remove(coin)
            elif self.player.rect.colliderect(coin.rect):
                self.coin_score += 10
                self.coins.remove(coin)

    def _spawn_pattern(self):
        p = random.random()
        start_y = -400
        new_entities = []
        
        if p < 0.4: # Simple obstacle
            new_entities.append(Obstacle(self.speed))
        elif p < 0.7: # Row of coins
            lane = random.randint(0, 2)
            for i in range(8):
                new_entities.append(Coin(lane, start_y - i*60, self.speed))
        elif p < 0.9: # Staggered barriers
            lanes = [0, 1, 2]
            random.shuffle(lanes)
            new_entities.append(Obstacle(self.speed, type="BLOCK", lane=lanes[0]))
            new_entities.append(Obstacle(self.speed, type="BLOCK", lane=lanes[1]))
        else: # Special: Jump & Slide Combo
            lane = random.randint(0, 2)
            new_entities.append(Obstacle(self.speed, type="JUMP", lane=lane))
            # Spawn coins above the jump obstacle
            for i in range(3):
                new_entities.append(Coin(lane, start_y - 200 - i*40, self.speed))

        # Filter new entities to prevent overlap with existing ones
        for entity in new_entities:
            if self._is_safe_to_spawn(entity):
                if isinstance(entity, Obstacle):
                    self.obstacles.append(entity)
                else:
                    self.coins.append(entity)

    def _is_safe_to_spawn(self, new_entity):
        # Buffer for safety
        buffer = 20
        safe_rect = new_entity.rect.inflate(buffer, buffer)
        
        for obs in self.obstacles:
            if safe_rect.colliderect(obs.rect):
                return False
        for coin in self.coins:
            if safe_rect.colliderect(coin.rect):
                return False
        return True

    def _draw(self):
        self.screen.fill(BG_COLOR)
        
        # Draw Lanes
        for lane_x in LANES:
            pygame.draw.line(self.screen, LANE_COLOR, (lane_x, 0), (lane_x, SCREEN_HEIGHT), 2)
            
        # Draw Entities
        for coin in self.coins:
            coin.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        self.player.draw(self.screen)
        
        # Draw UI
        self._draw_ui()
        
        if self.game_over:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_ui(self):
        # Score
        score_surf = self.font.render(f"SCORE: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_surf, (20, 20))
        
        # Coins
        coin_surf = self.font.render(f"COINS: {self.coin_score}", True, COIN_COLOR)
        self.screen.blit(coin_surf, (20, 60))
        
        # Instructions (Bottom Right)
        instructions = [
            "1 Finger: LANE 1",
            "2 Fingers: LANE 2",
            "3 Fingers: LANE 3",
            "4 Fingers: JUMP",
            "Fist: SLIDE"
        ]
        max_w = max(self.small_font.size(t)[0] for t in instructions)
        total_h = len(instructions) * 25
        bg_surface = pygame.Surface((max_w + 20, total_h + 10), pygame.SRCALPHA)
        bg_surface.fill((30, 30, 45, 180))
        self.screen.blit(bg_surface, (SCREEN_WIDTH - max_w - 30, SCREEN_HEIGHT - total_h - 30))
        
        for i, text in enumerate(instructions):
            instr_surface = self.small_font.render(text, True, (200, 200, 200))
            x = SCREEN_WIDTH - instr_surface.get_width() - 20
            y = SCREEN_HEIGHT - (len(instructions) - i) * 25 - 20
            self.screen.blit(instr_surface, (x, y))

    def _draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0,0))
        
        go_text = self.font.render("GAME OVER", True, OBSTACLE_BLOCK_COLOR)
        res_text = self.font.render(f"Final Score: {self.score + self.coin_score}", True, TEXT_COLOR)
        restart_text = self.font.render("Press 'R' to Restart", True, TEXT_COLOR)
        
        self.screen.blit(go_text, (SCREEN_WIDTH//2 - go_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
        self.screen.blit(res_text, (SCREEN_WIDTH//2 - res_text.get_width()//2, SCREEN_HEIGHT//2))
        self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
