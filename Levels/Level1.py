import pygame
import webbrowser
import math
import time

# Initialize the mixer
pygame.mixer.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, screen_rect):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_rect.centerx
        self.rect.centery = screen_rect.centery
        self.mask = pygame.mask.from_surface(self.image)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = 100
        self.mask = pygame.mask.from_surface(self.image)

class ChaseGame:
    def __init__(self):
        self.SCREEN_WIDTH = 1220
        self.SCREEN_HEIGHT = 660
        self.WHITE = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Meow_Level 1")

        self.background = pygame.image.load(r"world/level1_map.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.player = Player(r"characters/player1.png", self.screen.get_rect())
        self.enemy = Enemy(r"characters/enemy1.png")

        # 停止先前的音樂（如果有）
        if pygame.mixer.get_busy():
            pygame.mixer.stop()

        # 播放新的音樂
        self.music = pygame.mixer.Sound(r"music/maou_level1.mp3")
        self.music.play()

        self.player_speed = 10
        self.enemy_speed = 8
        self.enemy_delay = 1 * 60
        self.game_state = "playing"
        self.running = True
        self.enemy_started = False

        self.start_time = time.time()
        self.timer_duration = 5
        self.level_failed = False 
        self.level_complete = False

    def normalize(self, vector):
        mag = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        if mag > 0:
            return (vector[0] / mag, vector[1] / mag)
        return (0, 0)
    
    def draw_timer(self):
        current_time = time.time()
        remaining_time = max(0, self.timer_duration - (current_time - self.start_time))
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Time Left: {int(remaining_time)} seconds", True, (255, 255, 255))
        self.screen.blit(text, (5, 5))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_state == "paused":
                    self.game_state = "playing"
                    self.reset_positions()

    def reset_positions(self):
        self.player.rect.centerx = self.SCREEN_WIDTH // 2
        self.player.rect.centery = self.SCREEN_HEIGHT // 2
        self.enemy.rect.centerx = 100
        self.enemy.rect.centery = 100

    def update_player_position(self, keys):
        if keys[pygame.K_LEFT] and self.player.rect.left > 0:
            self.player.rect.x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player.rect.right < self.SCREEN_WIDTH:
            self.player.rect.x += self.player_speed
        if keys[pygame.K_UP] and self.player.rect.top > 0:
            self.player.rect.y -= self.player_speed
        if keys[pygame.K_DOWN] and self.player.rect.bottom < self.SCREEN_HEIGHT:
            self.player.rect.y += self.player_speed

    def handle_collisions(self):
        collided_enemies = pygame.sprite.spritecollide(self.player, [self.enemy], False, pygame.sprite.collide_mask)
        if collided_enemies and self.game_state == "playing":
            webbrowser.open("https://www.youtube.com/watch?v=xvFZjo5PgG0&ab_channel=Duran")
            self.game_state = "paused"
            self.level_failed = True
            self.music.stop()
            
    def move_enemy(self):
        if not self.enemy_started:
            self.enemy_delay -= 1
            if self.enemy_delay <= 0:
                self.enemy_started = True

        if self.enemy_started and self.game_state == "playing":
            dx = self.player.rect.centerx - self.enemy.rect.centerx
            dy = self.player.rect.centery - self.enemy.rect.centery
            dx, dy = self.normalize((dx, dy))
            self.enemy.rect.x += dx * self.enemy_speed
            self.enemy.rect.y += dy * self.enemy_speed

    def update(self):
        keys = pygame.key.get_pressed()
        self.handle_events()

        if self.game_state == "playing":
            self.update_player_position(keys)
            self.handle_collisions()
            self.move_enemy()
            self.check_timer()


        self.player.rect.clamp_ip(self.screen.get_rect())
        self.enemy.rect.clamp_ip(self.screen.get_rect())
    
    def check_timer(self):
        current_time = time.time()
        remaining_time = max(0, self.timer_duration - (current_time - self.start_time))
        if remaining_time <= 0:
            if not self.level_failed:
                self.level_complete = True
            self.game_state = "paused"
            self.running = False

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.draw_timer()
        if self.game_state == "paused":  # 只在遊戲暫停時繪製 "Time's up!" 文字
            font = pygame.font.SysFont(None, 48)
            text = font.render("Goody-Goody ^^b", True, (0, 0, 255))
            screen.blit(text, (self.SCREEN_WIDTH // 2 - 100, self.SCREEN_HEIGHT // 2))
        screen.blit(self.player.image, self.player.rect)
        screen.blit(self.enemy.image, self.enemy.rect)


    def is_complete(self):
        return self.level_complete and not self.level_failed
    
    def is_failed(self):
        return self.level_failed
   
    def cleanup(self):
        pass

game_instance = ChaseGame()

def init():
    global game_instance
    game_instance = ChaseGame()

def update():
    game_instance.update()

def draw(screen):
    game_instance.draw(screen)

def is_complete():
    return game_instance.is_complete()

def is_failed():  # 添加這個函數
    global game_instance
    return game_instance.is_failed()

def cleanup():
    game_instance.cleanup()
