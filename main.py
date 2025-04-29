import sys
import os
import pygame
import Levels.Level1 as level1
import Levels.Level2 as level2
import Levels.Level3 as level3

# 將專案根目錄添加到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# 初始化 Pygame
pygame.init()

# 設定螢幕
screen = pygame.display.set_mode((1220, 660))
font = pygame.font.Font(None, 36)

def show_message(screen, message, duration=2000):
    screen.fill((255, 255, 255))  # 將背景填滿白色（255, 255, 255）
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2)) # 文字位置
    screen.blit(text, text_rect) # 將文字圖像繪製到螢幕上指定的位置
    pygame.display.flip() # 把上面設定好的內容都更新到螢幕
    pygame.time.wait(duration) # 暫停時間長度 # 訊息顯示的時間（以毫秒為單位），預設為2000毫秒（2秒）

# 製作換關之間的按鈕，後面參數為設定按鈕設計
def draw_button(screen, text, x, y, w, h, inactive_color, active_color, font, is_last_level):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # 計算按鈕的中心點位置
    button_center = (screen.get_width() / 2 - w / 2, y)

    # 檢查滑鼠是否在按鈕範圍內
    if button_center[0] + w > mouse[0] > button_center[0] and button_center[1] + h > mouse[1] > button_center[1]:
        pygame.draw.rect(screen, active_color, (button_center[0], button_center[1], w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (button_center[0], button_center[1], w, h))

    if is_last_level: # 判斷是否為最後一關
        text = "YOU HAVE FINISHED ALL THE LEVELS!"
        # 最後一關通過，就會跳出完成所有關卡訊息

    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(button_center[0] + w / 2, button_center[1] + h / 2))
    screen.blit(text_surface, text_rect)
    return False

def main():
    running = True
    game_started = False  # 新增此變數以控制遊戲是否已經開始
    current_level = 0
    levels = [level1, level2, level3]

    # 成功過關圖片
    image = pygame.image.load(r"game_pic/thunbsup.png")  
    image = pygame.transform.scale(image, (358, 363))
    image_rect = image.get_rect()

    # 失敗嘲諷圖片
    image_lose = pygame.image.load(r"game_pic/lose.png")  
    image_lose = pygame.transform.scale(image_lose, (358, 363))
    image_lose_rect = image_lose.get_rect()


    while running: # 控制主遊戲循環是否繼續
        if not game_started:  # 新增這部分來顯示「Start Game」按鈕
            screen.fill((255, 255, 255))  # 填充白色背景
            if draw_button(screen, "Start Game", 80, 250, 600, 100, (103, 143, 141), (0, 255, 0), font, False):
             # 按鈕的水平位置（x坐標）、按鈕的垂直位置（y坐標）、按鈕的寬度、按鈕的高度、按鈕的顏色、按鈕被按下時的顏色
                game_started = True # 按鈕被按下，game_started 設定為True，代表遊戲開始！
                
            for event in pygame.event.get():    # 迭代處理所有Pygame事件
                if event.type == pygame.QUIT:   # 如果退出遊戲，狀態設置為false（要按叉叉的意思）
                            running = False 
                    
            pygame.display.flip()    # 更新螢幕顯示
            pygame.time.Clock().tick(60) # 控制遊戲循環每秒執行60次
            continue
        
        level = levels[current_level]  # 獲取當前關卡
        level.init()   # 初始化當前關卡

        level_running = True  # 控制當前關卡循環是否繼續
        while level_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    level_running = False

            level.update()
            level.draw(screen)
            
            if level.is_complete():
                level_running = False
                while True:
                    screen.fill((255, 255, 255))  # 填充白色背景
                    # 畫圖片在按鈕上方
                    image_rect.midbottom = (617, 425)  # 按鈕的 y 坐標是 425，圖片底部應該在 405 的位置 # 會跟遊戲畫面大小有關
                    screen.blit(image, image_rect)

                    if draw_button(screen, "Click to enter next level", 80, 425, 600, 100,  (103, 143, 141), (255, 208, 0), font,current_level == len(levels) - 1):
                        current_level += 1
                        break
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            level_running = False
                            break
                    pygame.display.flip()
                    pygame.time.Clock().tick(60)

            if level.is_failed():  # 假設這個方法用於檢查關卡是否失敗
                level_running = False
                while True:
                    screen.fill((255, 255, 255))  # 填充白色背景
                    # 畫圖片在按鈕上方
                    image_lose_rect.midbottom = (610, 425)  # 按鈕的 y 坐標是 425，圖片底部應該在 405 的位置
                    screen.blit(image_lose, image_lose_rect)

                    if draw_button(screen, "YOU LOSE", 80, 425, 300, 100,  (103, 143, 141), (255, 0, 0), font, False):
                        #按鈕的 x 座標位置(左上角相對於螢幕左邊緣的距離)、按鈕的 y 座標位置(左上角相對於螢幕頂邊緣的距離)、按鈕的寬度、 按鈕的高度
                        #level.reset()  # 重置關卡
                        break
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            level_running = False
                            break
                    pygame.display.flip()
                    pygame.time.Clock().tick(60)  # 控制遊戲循環的速度，使遊戲以每秒 60 幀的速度運行
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        level.cleanup()
    
    pygame.quit()

if __name__ == "__main__":
    main()
