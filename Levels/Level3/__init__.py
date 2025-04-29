import pygame
from Levels.Level3.Chase_setting import *
from Levels.Level3.Chase_player import Player
from Levels.Level3.Chase_enemy import Enemy
from Levels.Level3.Chase_kim import Kim
from Levels.Level3.Chase_sprite import Generic, Tree
from Levels.Level3.Chase_level import Level
from Levels.Level3.main import Game

game_instance = None

def init():
    global game_instance
    game_instance = Game()

def update():
    global game_instance
    game_instance.update()

def draw(screen):
    global game_instance
    game_instance.draw(screen)

def is_complete():
    global game_instance
    return game_instance.is_complete()

def is_failed():  # 添加這個函數
    global game_instance
    return game_instance.is_failed()

def cleanup():
    global game_instance
    game_instance.cleanup()