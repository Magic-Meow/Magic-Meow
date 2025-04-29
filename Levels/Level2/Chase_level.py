import pygame
from os import *
from Levels.Level2.Chase_setting import *
from Levels.Level2.Chase_player import Player
from Levels.Level2.Chase_enemy import Enemy
from pytmx.util_pygame import load_pygame
from Levels.Level2.Chase_sprite import Generic,Tree
import webbrowser

TILE_SIZE = 128  #會影響匯入上層物件大小

class Level:
	def __init__(self):
		# get the display surface
		self.display_surface = pygame.display.get_surface()
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.game_state = "playing"
		self.setup()  #這是為啥
		self.paused = False
		
		# 停止先前的音樂（如果有）
		if pygame.mixer.get_busy():
			pygame.mixer.stop()
			
		# 播放新的音樂
		self.music = pygame.mixer.Sound(r"music/maou_level2.mp3")
		# 設定音量（例如設置為 50% 音量）
		self.music.set_volume(4)
		self.music.play()

	def handle_collisions(self):
		collided_enemies = pygame.sprite.spritecollide(self.player, [self.enemy], False, pygame.sprite.collide_mask)
		if collided_enemies and self.game_state == "playing":
			webbrowser.open("https://www.youtube.com/shorts/DCiboeNZ7uw")
			self.game_state = "paused"
			self.paused = True  # 遊戲暫停
			self.music.stop()
			self.pause_time = pygame.time.get_ticks()  # 紀錄暫停時間
	
	def setup(self):
		tmx_data = load_pygame(r"world/tiled/level2_tmx.tmx")
		
		Generic(
			pos = (0,0),
			surf = pygame.image.load(r"world/level2_map.png").convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground']) 
		# Player 
		for obj in tmx_data.get_layer_by_name('player'):
			if obj.name == 'start':
				#self.player = Player((obj.x,obj.y), self.all_sprites,self.collision_sprites) #加進去變成兩隻！
				self.player = Player((900,300), self.all_sprites,self.collision_sprites)  #上面創的那個拉近來
		# Enemy 
		for obj in tmx_data.get_layer_by_name('enemy'):
			if obj.name == 'start_enemy':
				#self.enemy = Enemy((obj.x,obj.y), self.all_sprites,self.collision_sprites) #加進去變成兩隻！
				self.enemy = Enemy((600,400), self.all_sprites,self.collision_sprites)  #上面創的那個拉近來

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
	
	def run(self,dt):
		self.display_surface.fill((234,218,183))
		self.all_sprites.custom_draw(self.player, self.enemy)
		self.handle_collisions()  # 在適當位置呼叫碰撞處理
		player_pos = self.player.rect.center  # 獲取玩家位置信息
		self.enemy.enemy_update(dt, player_pos)  # 傳遞玩家位置給敵人對象
		self.all_sprites.update(dt)

class CameraGroup(pygame.sprite.Group):
		def __init__(self):
			super().__init__()
			self.display_surface = pygame.display.get_surface()
			self.offset = pygame.math.Vector2()
		
		def custom_draw(self, player, enemy):
			self.player_offset = player.rect.center - pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
			self.enemy_offset = enemy.rect.center - pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
			self.offset = (self.player_offset + self.enemy_offset) / 2
	
			for layer in LAYERS.values():
				for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
					if sprite.z == layer:
						offset_rect = sprite.rect.copy()
						offset_rect.center -= self.offset
						self.display_surface.blit(sprite.image, offset_rect)
