"""Game constants"""

# Screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

# Colors
BG_COLOR = (20, 20, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 50)
ORANGE = (255, 165, 0)
GRAY = (150, 150, 150)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
PURPLE = (200, 50, 255)
PINK = (255, 192, 203)
LIME = (50, 205, 50)
TEAL = (0, 128, 128)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
DARK_RED = (139, 0, 0)
DARK_BLUE = (0, 0, 139)

# Player
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80
PLAYER_SPEED = 5
PLAYER_JUMP_POWER = 15
GRAVITY = 0.5

# Weapons stats
WEAPONS = {
    "sword": {"damage": 15, "color": SILVER, "width": 40, "height": 10},
    "mace": {"damage": 20, "color": (180, 100, 50), "width": 35, "height": 15},
    "stick": {"damage": 10, "color": (139, 69, 19), "width": 50, "height": 8},
    "axe": {"damage": 25, "color": GOLD, "width": 38, "height": 18},
    "spear": {"damage": 18, "color": CYAN, "width": 55, "height": 9},
    "hammer": {"damage": 22, "color": (139, 69, 19), "width": 32, "height": 20},
    "dagger": {"damage": 12, "color": (200, 100, 100), "width": 25, "height": 8},
    "scythe": {"damage": 23, "color": DARK_RED, "width": 45, "height": 14},
    "whip": {"damage": 16, "color": (184, 134, 11), "width": 48, "height": 6},
    "staff": {"damage": 17, "color": PURPLE, "width": 52, "height": 10}
}

# Enemy
ENEMY_AI_UPDATE_FREQ = 30  # frames between AI decisions

# Maps
MAPS = {
    "Arena": {"bg_color": (20, 20, 40), "accent_color": (100, 100, 150), "name": "Dark Arena"},
    "Forest": {"bg_color": (34, 80, 34), "accent_color": (50, 150, 50), "name": "Enchanted Forest"},
    "Desert": {"bg_color": (220, 180, 60), "accent_color": (200, 150, 30), "name": "Sandy Desert"},
    "Ice": {"bg_color": (100, 180, 255), "accent_color": (150, 200, 255), "name": "Frozen Tundra"},
    "Volcano": {"bg_color": (80, 40, 20), "accent_color": (255, 100, 30), "name": "Volcanic Crater"},
    "Castle": {"bg_color": (60, 60, 80), "accent_color": (100, 100, 150), "name": "Ancient Castle"}
}

# Difficulty Settings
DIFFICULTY_LEVELS = {
    "easy": {
        "enemy_health": 80,
        "enemy_damage_multiplier": 0.7,
        "enemy_speed": 3,
        "enemy_ai_update_freq": 50,
        "player_health": 150
    },
    "normal": {
        "enemy_health": 100,
        "enemy_damage_multiplier": 1.0,
        "enemy_speed": 5,
        "enemy_ai_update_freq": 30,
        "player_health": 100
    },
    "hard": {
        "enemy_health": 120,
        "enemy_damage_multiplier": 1.3,
        "enemy_speed": 6,
        "enemy_ai_update_freq": 20,
        "player_health": 80
    },
    "insane": {
        "enemy_health": 150,
        "enemy_damage_multiplier": 1.6,
        "enemy_speed": 7,
        "enemy_ai_update_freq": 15,
        "player_health": 60
    }
}
