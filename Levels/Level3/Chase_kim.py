import pygame 
from Levels.Level3.Chase_setting import *
from Levels.Level3.Chase_support import *
import math

class Kim(pygame.sprite.Sprite):
	def __init__(self, pos, group, collision_sprites):
		super().__init__(group)
		
		self.status = 'kim'
		self.frame_index = 0
		self.image = pygame.image.load(r"characters/kim3.png")
		self.mask = pygame.mask.from_surface(self.image)
		# general setup
		
		self.rect = self.image.get_rect(center = pos) #跟position有關 #放在長方形中間
		
		self.z = LAYERS['main']

        # movement attributes
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 150
		self.kim_started = False
		self.kim_delay = 60
		
		#collision
		self.hitbox = self.rect.copy().inflate((0,20)) #要跟下面def move 一起 #藉由增加圖片框框寬度製作撞擊
		self.collision_sprites = collision_sprites

	def collision_kim(self, direction):
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
	
	def move_kim(self, dt, player_pos):
		if not self.kim_started:
			self.kim_delay -= 1
			if self.kim_delay <= 0:
				self.kim_started = True
		if self.kim_started:
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
			self.collision_kim('horizontal')
            # vertical movement 走垂直
			self.pos.y += self.direction.y * self.speed * dt
			self.hitbox.centery = round(self.pos.y)
			self.rect.centery = self.hitbox.centery
			self.collision_kim('vertical')
			self.pos += self.direction * self.speed * dt
			self.rect.center = self.pos
		
	def kim_update(self, dt, player_pos):
		# self.input()
		self.move_kim(dt,player_pos)