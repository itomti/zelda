import pygame

# game setup
WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64

# User interface
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT_PATH = 'assets/font/joystix.ttf'
UI_FONT_SIZE = 18

# General colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

WORLD_MAP = [
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ','p',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ','x','x','x','x','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ','x'],
['x',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x','x','x',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ','x',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ','x','x','x','x','x',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ','x','x','x',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
]


def import_weapon_data():
    weapon_data = {
        'axe': {
            'cooldown': 300,
            'damage': 20,
            'direction_surfaces': {
                'left': pygame.image.load('assets/weapons/axe/left.png').convert_alpha(),
                'up': pygame.image.load('assets/weapons/axe/up.png').convert_alpha(),
                'right': pygame.image.load('assets/weapons/axe/right.png').convert_alpha(),
                'down': pygame.image.load('assets/weapons/axe/down.png').convert_alpha(),
                'full': pygame.image.load('assets/weapons/axe/full.png').convert_alpha()
            }
        },
        'lance': {
            'cooldown': 400,
            'damage': 30,
            'direction_surfaces': {
                'left': pygame.image.load('assets/weapons/lance/left.png').convert_alpha(),
                'up': pygame.image.load('assets/weapons/lance/up.png').convert_alpha(),
                'right': pygame.image.load('assets/weapons/lance/right.png').convert_alpha(),
                'down': pygame.image.load('assets/weapons/lance/down.png').convert_alpha(),
                'full': pygame.image.load('assets/weapons/lance/full.png').convert_alpha()
            }
        },
        'rapier': {
            'cooldown': 300,
            'damage': 20,
            'direction_surfaces': {
                'left': pygame.image.load('assets/weapons/rapier/left.png').convert_alpha(),
                'up': pygame.image.load('assets/weapons/rapier/up.png').convert_alpha(),
                'right': pygame.image.load('assets/weapons/rapier/right.png').convert_alpha(),
                'down': pygame.image.load('assets/weapons/rapier/down.png').convert_alpha(),
                'full': pygame.image.load('assets/weapons/rapier/full.png').convert_alpha()
            }
        },
        'sai': {
            'cooldown': 80,
            'damage': 10,
            'direction_surfaces': {
                'left': pygame.image.load('assets/weapons/sai/left.png').convert_alpha(),
                'up': pygame.image.load('assets/weapons/sai/up.png').convert_alpha(),
                'right': pygame.image.load('assets/weapons/sai/right.png').convert_alpha(),
                'down': pygame.image.load('assets/weapons/sai/down.png').convert_alpha(),
                'full': pygame.image.load('assets/weapons/sai/full.png').convert_alpha()
            }
        },
        'sword': {
            'cooldown': 100,
            'damage': 15,
            'direction_surfaces': {
                'left': pygame.image.load('assets/weapons/sword/left.png').convert_alpha(),
                'up': pygame.image.load('assets/weapons/sword/up.png').convert_alpha(),
                'right': pygame.image.load('assets/weapons/sword/right.png').convert_alpha(),
                'down': pygame.image.load('assets/weapons/sword/down.png').convert_alpha(),
                'full': pygame.image.load('assets/weapons/sword/full.png').convert_alpha()
            }
        }
    }
    return weapon_data


def import_magic_data() -> dict:
    magic_data = {
        'flame': {'strength': 5, 'cost': 20, 'graphic': pygame.image.load('assets/graphics/particles/flame/fire.png')},
        'heal': {'strength': 20, 'cost': 10, 'graphic': pygame.image.load('assets/graphics/particles/heal/heal.png')}
    }

    return magic_data