import pygame
import sys
from Levels.Level3.Chase_setting import *
from Levels.Level3.Chase_level import Level
import time

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption('Meow_Level 3')
        self.clock = pygame.time.Clock()
        
        self.level = Level()
        self.start_time = pygame.time.get_ticks()
        self.remaining_time = 5  # 設定初始剩餘時間為60秒
        self.paused = False
        self.level_complete = False
        self.level_failed = False

    def run(self):
            while self.remaining_time > 0:  # 當剩餘時間大於0時執行遊戲
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.level_failed = True
                        return  # 直接返回，結束當前關卡

                if not self.paused:  # 只有在遊戲不處於暫停狀態時才更新時間
                    dt = self.clock.tick() / 1000
                    self.level.run(dt)

                    # 計算經過的時間
                    if not self.level.game_state == "paused":
                        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
                    else:
                        self.level_failed = True
                        return  # 直接返回，結束當前關卡

                    self.remaining_time = 5 - elapsed_time 

                # 顯示計時器在螢幕上
                font = pygame.font.SysFont(None, 36)
                text = font.render(f"Time Left: {str(self.remaining_time)} seconds", True, (255, 255, 255))
                self.screen.blit(text, (10, 10))

                pygame.display.update()

            if self.remaining_time <= 0 and not self.level_failed:
                self.level_complete = True

            # 結束遊戲時顯示"Time's up!"
            font = pygame.font.SysFont(None, 48)
            text = font.render("Time's up!", True, (255, 0, 0))
            self.screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            pygame.display.update()
            pygame.time.wait(2000)  # 等待2秒後退出遊戲

        # pygame.quit()
        # sys.exit()

    def update(self):
        self.run()  # 將原來的 run 函數邏輯放在 update 中

    def draw(self, screen):
        self.level.run(self.clock.tick() / 1000)  # 更新並繪製
        pygame.display.update()

    def is_complete(self):
        print(f"is_complete called, level_complete: {self.level_complete}, level_failed: {self.level_failed}")
        return self.level_complete and not self.level_failed
    
    def is_failed(self):
        return self.level_failed

    def cleanup(self):
        pass