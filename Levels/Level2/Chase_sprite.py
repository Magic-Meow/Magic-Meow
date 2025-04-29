import pygame
from Levels.Level2.Chase_setting import *

class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf,groups, z = LAYERS['main']):#讓layer預設值在main上面
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Tree(Generic):
	def __init__(self, pos, surf,groups, name):
		super().__init__(pos, surf, groups)
		