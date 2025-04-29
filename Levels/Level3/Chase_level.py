import pygame
from os import *
from Levels.Level3.Chase_setting import *
from Levels.Level3.Chase_player import Player
from Levels.Level3.Chase_enemy import Enemy
from Levels.Level3.Chase_kim import Kim
from pytmx.util_pygame import load_pygame
from Levels.Level3.Chase_sprite import Generic,Tree, Interaction
import webbrowser

TILE_SIZE = 64 #會影響匯入上層物件大小

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group() # PYGAME裡面所有物件
        self.interaction_sprites = pygame.sprite.Group()
        self.game_state = "playing"
        self.setup()  #這是為啥???	
    
        # 停止先前的音樂（如果有）
        if pygame.mixer.get_busy():
            pygame.mixer.stop()
            
        # 播放新的音樂
        self.music = pygame.mixer.Sound(r"music/maou_level3.mp3")
        self.music.play()

    
    def handle_collisions(self):
        collided_enemies = pygame.sprite.spritecollide(self.player, [self.enemy], False, pygame.sprite.collide_mask)
        if collided_enemies and self.game_state == "playing":
            webbrowser.open("https://www.youtube.com/shorts/IOPnXCbBx3w")
            self.game_state = "paused"
            self.music.stop()
    
    def handle_kim(self):
        collided_kim = pygame.sprite.spritecollide(self.player, [self.kim], False, pygame.sprite.collide_mask)
        if collided_kim and self.game_state == "playing":
            webbrowser.open("https://www.youtube.com/watch?v=vDnW1okFx9w&ab_channel=%E6%9D%B1%E5%90%B3%E5%A4%A7%E5%AD%B8%E5%B7%A8%E9%87%8F%E8%B3%87%E6%96%99%E7%AE%A1%E7%90%86%E5%AD%B8%E9%99%A2%E8%B3%87%E6%96%99%E7%A7%91%E5%AD%B8%E7%B3%BB")
            self.game_state = "paused"
            self.music.stop()

    def setup(self):
        tmx_data = load_pygame(r"world/tiled/level3_tmx.tmx")
        
        Generic(
            pos = (0,0),
            surf = pygame.image.load(r"world/level3_map.png").convert_alpha(),
            groups = self.all_sprites,
            z = LAYERS['ground']) 
    
        # Player 
        for obj in tmx_data.get_layer_by_name('player'):
            if obj.name == 'start':
                self.player = Player((obj.x,obj.y), self.all_sprites,self.collision_sprites) #加進去變成兩隻！
                #self.player = Player((0,10), self.all_sprites,self.collision_sprites)  #上面創的那個拉近來
            # if obj.name == "enemy":
            # 	Interaction((obj.x,obj.y), (obj.width,obj.height),self.interaction_sprites, obj.name)

        # Enemy 
        for obj in tmx_data.get_layer_by_name('enemy'):
            if obj.name == 'start_enemy':
                self.enemy = Enemy((obj.x,obj.y), self.all_sprites,self.collision_sprites) #加進去變成兩隻！
                #self.enemy = Enemy((600,400), self.all_sprites,self.collision_sprites)  #上面創的那個拉近來

        # Kim
        for obj in tmx_data.get_layer_by_name('kim'):
            if obj.name == 'start_kim':
                self.kim = Kim((obj.x,obj.y), self.all_sprites,self.collision_sprites) #加進去變成兩隻！
                #self.kim = Kim((900,800), self.all_sprites,self.collision_sprites)  #上面創的那個拉近來


        # get layers 
        print(tmx_data.layers) # get all layers 
        for layer in tmx_data.visible_layers: # get visible layers 
            print(layer)

        # trees 
        for layer in ['plants and rocks']:  #匯入這個layer的東西
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE,y * TILE_SIZE), surf, self.all_sprites, LAYERS['main'])
        
        for obj in tmx_data.get_layer_by_name('trees'):
            Tree((obj.x, obj.y), obj.image, [self.all_sprites,self.collision_sprites], obj.name)
            #player要擺在下面，才會出現在上面！
          
        # collion tiles 
        for x, y, surf in tmx_data.get_layer_by_name('collision').tiles():
             Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)
                
        #  #collion tiles視覺化
        # for x, y, surf in tmx_data.get_layer_by_name('collision').tiles():
        # 	Generic((x * TILE_SIZE, y * TILE_SIZE),  surf, self.all_sprites, LAYERS['main'])
        
    def run(self,dt):
        self.display_surface.fill((234,218,183))
        self.all_sprites.custom_draw(self.player, self.enemy, self.kim)
        self.handle_collisions()  # 在適當位置呼叫碰撞處理
        self.handle_kim()
        player_pos = self.player.rect.center  # 獲取玩家位置
        self.kim.kim_update(dt, player_pos)  # 傳遞玩家位置給敵人對象
        self.enemy.enemy_update(dt, player_pos)  # 傳遞玩家位置給敵人對象
        self.all_sprites.update(dt)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
    
    def custom_draw(self, player, enemy, kim):
        self.player_offset = player.rect.center - pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.enemy_offset = enemy.rect.center - pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.kim_offset = kim.rect.center - pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        # self.offset = (self.player_offset + self.enemy_offset) / 2
        self.offset = (self.player_offset + self.enemy_offset + self.kim_offset) / 3
        # self.player_offset_x = player.rect.centerx - SCREEN_WIDTH / 2
        # self.player_offset_y = player.rect.centery - SCREEN_HEIGHT / 2

        # self.enemy_offset_x = enemy.rect.centerx - SCREEN_WIDTH / 2
        # self.enemy_offset_y = enemy.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)