from pygame.math import Vector2
# screen
SCREEN_WIDTH = 1220
SCREEN_HEIGHT = 660
TILE_SIZE = 64


player_speed = 2 #
enemy_speed = 1 #
enemy_delay = 3 * 60 #
game_state = "playing" #
running = True #
enemy_started = False #

LAYERS = {

	'ground': 1,
	'main': 2
#數字越大越晚畫進去
}

RUN_SPEED = {
	'player_speed' : 2, #
    'enemy_speed' : 1, #
    'enemy_delay' : 3 * 60, #
}