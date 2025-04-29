# class Enemy(pygame.sprite.Sprite):
# 	def __init__(self, pos, group, collision_sprites):
# 		super().__init__(group)
		
# 		self.status = 'enemy'
# 		self.frame_index = 0
# 		self.image = pygame.image.load(r"C:\Users\zhiya\Downloads\jutta_yaotry\pic\enemy.png")
        
# 		# general setup
		
# 		self.rect = self.image.get_rect(center = pos) #跟position有關 #放在長方形中間
# 		self.mask = pygame.mask.from_surface(self.image)

# 		self.z = LAYERS['main']

#         movement attributes
# 		self.direction = pygame.math.Vector2()
# 		self.pos = pygame.math.Vector2(self.rect.center)
# 		self.speed = 200
		
# 		collision
# 		self.hitbox = self.rect.copy().inflate((-126,-70)) #要跟下面def move 一起 #藉由增加圖片框框寬度製作撞擊
# 		self.collision_sprites = collision_sprites

##############################
import pygame 
from Levels.Level3.Chase_setting import *
from Levels.Level3.Chase_support import *
import math

class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos, group, collision_sprites):
		super().__init__(group)
		
		self.status = 'enemy'
		self.frame_index = 0
		self.image = pygame.image.load(r"characters/enemy3.png")
		self.mask = pygame.mask.from_surface(self.image)
		# general setup
		
		self.rect = self.image.get_rect(center = pos) #跟position有關 #放在長方形中間
		
		self.z = LAYERS['main']

        # movement attributes
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 100
		self.enemy_started = False
		self.enemy_delay = 100
		
		#collision
		self.hitbox = self.rect.copy().inflate((0,20)) #要跟下面def move 一起 #藉由增加圖片框框寬度製作撞擊
		self.collision_sprites = collision_sprites

	def collision_enemy(self, direction):
		for sprite in self.collision_sprites.sprites(): 
			if hasattr(sprite, 'hitbox'):  #看看有沒有hitbox這個屬性
				if sprite.hitbox.colliderect(self.hitbox):  #如果有就要
					if direction == 'horizontal': #水平
						if self.direction.x > 0: # moving right  #辨別碰撞從哪個方向來
							self.hitbox.right = sprite.hitbox.left
						if self.direction.x < 0: # moving left
							self.hitbox.left = sprite.hitbox.right
						self.rect.centerx = self.hitbox.centerx
						self.pos.x = self.hitbox.centerx
					
					if direction == 'vertical':
						if self.direction.y > 0: # moving down
								self.hitbox.bottom = sprite.hitbox.top
						if self.direction.y < 0: # moving up
								self.hitbox.top = sprite.hitbox.bottom
						self.rect.centery = self.hitbox.centery
						self.pos.y = self.hitbox.centery
	def normalize(self, vec):
		length = math.sqrt(vec[0] ** 2 + vec[1] ** 2)
		if length != 0:
			return vec[0] / length, vec[1] / length
		return 0, 0

	# def input(self):
	# 	keys = pygame.key.get_pressed()  #回傳被按鈕的list
	# 	if keys[pygame.K_w]:   #控制上下左右
	# 		self.direction.y = -1
	# 	elif keys[pygame.K_s]:
	# 		self.direction.y = 1
	# 	else:
	# 		self.direction.y = 0

	# 	if keys[pygame.K_d]:
	# 		self.direction.x = 1
	# 	elif keys[pygame.K_a]:
	# 		self.direction.x = -1
	# 	else:
	# 		self.direction.x = 0
			
	def move_enemy(self, dt, player_pos):
		if not self.enemy_started:
			self.enemy_delay -= 1
			if self.enemy_delay <= 0:
				self.enemy_started = True
		if self.enemy_started:
			dx = player_pos[0] - self.rect.centerx
			dy = player_pos[1] - self.rect.centery
			dx, dy = self.normalize((dx, dy))
			self.direction = pygame.math.Vector2(dx, dy)

            # 走斜的話會比較快，所以要調整(1:1:根號2)
			if self.direction.magnitude() > 0:  # 如果方向是[0,0]=>沒指向任何地方
				self.direction = self.direction.normalize()

            # horizontal movement 走水平
			self.pos.x += self.direction.x * self.speed * dt
			self.hitbox.centerx = round(self.pos.x)
			self.rect.centerx = self.hitbox.centerx
			self.collision_enemy('horizontal')
            # vertical movement 走垂直
			self.pos.y += self.direction.y * self.speed * dt
			self.hitbox.centery = round(self.pos.y)
			self.rect.centery = self.hitbox.centery
			self.collision_enemy('vertical')
			self.pos += self.direction * self.speed * dt
			self.rect.center = self.pos
		
	def enemy_update(self, dt, player_pos):
		# self.input()
		self.move_enemy(dt,player_pos)

# class Enemy(pygame.sprite.Sprite):
#     def __init__(self, image_path):
#         super().__init__()
#         self.image = self.image = pygame.image.load(r"C:\Users\zhiya\Downloads\jutta_yaotry\pic\enemy.png")
#         self.rect = self.image.get_rect()
#         self.rect.centerx = 100
#         self.rect.centery = 100
        #self.mask = pygame.mask.from_surface(self.image)  # 创建精确的碰撞掩码

#	def update_player_position(self, keys):
#		if keys[pygame.K_LEFT] and self.rect.left > 0:
#			self.rect.x -= player_speed
#		if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
#			self.rect.x += player_speed
#		if keys[pygame.K_UP] and self.rect.top > 0:
#			self.rect.y -= player_speed
#		if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
#		    self.rect.y += player_speed
	