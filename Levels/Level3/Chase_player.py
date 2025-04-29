import pygame 
import webbrowser
from Levels.Level3.Chase_setting import *
from Levels.Level3.Chase_support import *

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group,collision_sprites):
		super().__init__(group)
		
		self.status = 'player'
		self.frame_index = 0
		self.image = pygame.image.load(r"characters/player3.png")
		self.mask = pygame.mask.from_surface(self.image)
		# general setup
		
		self.rect = self.image.get_rect(center = pos) #跟position有關 #放在長方形中間
		
		self.z = LAYERS['main']

        # movement attributes
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 300
		
		# self.interaction = interaction

		#collision
		self.hitbox = self.rect.copy().inflate((-126,-70)) #要跟下面def move 一起 #藉由增加圖片框框寬度製作撞擊
		self.collision_sprites = collision_sprites

	def collision(self, direction):
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

	def input(self):
		keys = pygame.key.get_pressed()  #回傳被按鈕的list
		if keys[pygame.K_UP]:   #控制上下左右
			self.direction.y = -1
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0
		
		# collided_interaction_sprite = pygame.sprite.spritecollide(self ,self.interaction ,False)
		# if collided_interaction_sprite:
		# 		if collided_interaction_sprite[0].name == 'enemy':
		# 			print("碰到了")
		# 		# webbrowser.open("https://www.youtube.com/watch?v=xvFZjo5PgG0&ab_channel=Duran")
				# else:
				# 	self.status = 'left_idle'
				# 	self.sleep = True
			
	def move(self,dt):
		# 走斜的話會比較快，所以要調整(1:1:根號2) 
		if self.direction.magnitude() > 0: #如果方向是[0,0]=>沒指向任何地方
			self.direction = self.direction.normalize()

			
		
        # horizontal movement 走水平
		self.pos.x += self.direction.x * self.speed * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		self.collision('horizontal')
		# vertical movement 走垂直
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')

		# 計算移動後的位置
		new_pos = self.pos + self.direction * self.speed * dt

		# 確保新位置在遊戲視窗範圍內
		if new_pos.x >= 0 and new_pos.x <= SCREEN_WIDTH - self.rect.width:
			self.pos.x = new_pos.x
		if new_pos.y >= 0 and new_pos.y <= SCREEN_HEIGHT - self.rect.height:
			self.pos.y = new_pos.y

		# 更新碰撞框和精靈位置
		self.hitbox.center = self.pos
		self.rect.center = self.pos
		
	def update(self, dt):
		self.input()
		self.move(dt)

#	def update_player_position(self, keys):
		# if keys[pygame.K_LEFT] and self.rect.left > 0:
		# 	self.rect.x -= player_speed
		# if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
		# 	self.rect.x += player_speed
		# if keys[pygame.K_UP] and self.rect.top > 0:
		# 	self.rect.y -= player_speed
		# if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
		#     self.rect.y += player_speed
	