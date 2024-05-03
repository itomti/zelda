import pygame

# game setup
WIDTH    = 1280
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

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