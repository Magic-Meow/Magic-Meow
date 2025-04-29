import pygame
from Levels.Level3.Chase_setting import *

class Generic(pygame.sprite.Sprite): # Generic 類 繼承 pygame.sprite.Sprite，是所有遊戲物件的基礎類別
	def __init__(self, pos, surf,groups, z = LAYERS['main']): # 初始化 # 讓 layer 預設值在main上面
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
		# hitbox 用於碰撞系統，檢測是否碰撞 
		### inflate >> 改變矩形對象（如 rect）尺寸。根據給定的值擴展或縮小矩形的寬度和高度。


class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name

		
class Tree(Generic):
	def __init__(self, pos, surf,groups,name):
		super().__init__(pos, surf, groups)
		# self.name = name
		