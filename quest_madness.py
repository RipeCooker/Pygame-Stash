import pygame
import random
import math
import sys
import json
import os as os_module

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# ============ CONSTANTS ============
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60
LEVEL_WIDTH = 4000  # Much longer levels

# Audio paths (using pygame's built-in example sounds)
import os
PYGAME_DATA_PATH = os.path.join(os.path.dirname(pygame.__file__), 'examples', 'data')
MUSIC_FILE = os.path.join(PYGAME_DATA_PATH, 'house_lo.ogg')
JUMP_SOUND = os.path.join(PYGAME_DATA_PATH, 'punch.wav')
COIN_SOUND = os.path.join(PYGAME_DATA_PATH, 'whiff.wav')
ENEMY_KILL_SOUND = os.path.join(PYGAME_DATA_PATH, 'boom.wav')

# Save file path for progress
SAVE_FILE = 'quest_madness_save.json'

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (20, 33, 61)
LIGHT_BLUE = (100, 150, 255)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
YELLOW = (255, 200, 50)
ORANGE = (255, 140, 0)
PURPLE = (200, 100, 255)
CYAN = (50, 200, 200)
GRAY = (100, 100, 100)

# Theme colors for different levels
LEVEL_THEMES = {
    1: {  # Grass level
        'bg': (34, 139, 34),  # Forest green
        'platform': (60, 180, 60),  # Grass green
        'platform_light': (120, 200, 100),  # Light grass
        'name': 'Grass Fields'
    },
    2: {  # Desert level
        'bg': (184, 134, 11),  # Dark goldenrod
        'platform': (210, 180, 140),  # Tan
        'platform_light': (238, 203, 173),  # Peach puff
        'name': 'Desert Wastes'
    },
    3: {  # Chamber/Cave level
        'bg': (25, 25, 112),  # Midnight blue
        'platform': (70, 70, 140),  # Slate blue
        'platform_light': (105, 105, 205),  # Medium slate blue
        'name': 'Crystal Chamber'
    }
}

# ============ SAVE/LOAD FUNCTIONS ============
def save_progress(player_stats):
    """Save game progress to file"""
    try:
        save_data = {
            'crystals': player_stats['crystals'],
            'coins': player_stats['coins'],
            'max_health': player_stats['max_health'],
            'speed_bonus': player_stats['speed_bonus'],
            'highest_level': player_stats.get('highest_level', 1)
        }
        with open(SAVE_FILE, 'w') as f:
            json.dump(save_data, f)
        print(f"Progress saved to {SAVE_FILE}")
    except Exception as e:
        print(f"Error saving progress: {e}")

def load_progress():
    """Load game progress from file"""
    try:
        if os_module.path.exists(SAVE_FILE):
            with open(SAVE_FILE, 'r') as f:
                save_data = json.load(f)
            return {
                'crystals': save_data.get('crystals', 0),
                'coins': save_data.get('coins', 0),
                'max_health': save_data.get('max_health', 100),
                'speed_bonus': save_data.get('speed_bonus', 0),
                'lives': 999,  # Infinite lives
                'highest_level': save_data.get('highest_level', 1)
            }
    except Exception as e:
        print(f"Error loading progress: {e}")
    
    # Return default stats if no save found
    return {
        'crystals': 0,
        'coins': 0,
        'max_health': 100,
        'speed_bonus': 0,
        'lives': 999,  # Infinite lives
        'highest_level': 1
    }

# ============ PARTICLE CLASS ============
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, vel_x, vel_y, lifetime=30):
        super().__init__()
        self.width = 5
        self.height = 5
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color

    def update(self):
        """Update particle physics"""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vel_y += 0.2  # Gravity
        self.lifetime -= 1
        
        # Fade out
        alpha = int((self.lifetime / self.max_lifetime) * 255)
        self.image.set_alpha(alpha)

# ============ CHECKPOINT CLASS ============
class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, x, y, checkpoint_id):
        super().__init__()
        self.width = 40
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(center=(x, y))
        self.checkpoint_id = checkpoint_id
        self.activated = False
        self.draw_checkpoint()

    def draw_checkpoint(self):
        """Draw checkpoint flag"""
        self.image.fill(DARK_BLUE)
        if self.activated:
            pygame.draw.rect(self.image, CYAN, (0, 0, self.width, self.height), 3)
            pygame.draw.polygon(self.image, CYAN, [(5, 5), (25, 10), (5, 15)])
        else:
            pygame.draw.rect(self.image, GRAY, (0, 0, self.width, self.height), 3)
            pygame.draw.polygon(self.image, GRAY, [(5, 5), (25, 10), (5, 15)])

    def activate(self):
        """Activate checkpoint"""
        self.activated = True
        self.draw_checkpoint()

# ============ PLAYER CLASS ============
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 30
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.spawn_x = x
        self.spawn_y = y
        self.checkpoint_x = x
        self.checkpoint_y = y
        
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = -12
        self.move_speed = 5
        self.on_ground = False
        self.on_wall = False
        self.wall_side = None  # 'left' or 'right'
        
        self.health = 100
        self.coins = 0
        self.crystals = 0
        self.score = 0
        self.alive = True
        self.facing_right = True
        self.draw_player()

    def draw_player(self):
        """Draw player as a square"""
        self.image.fill(YELLOW)
        pygame.draw.rect(self.image, WHITE, (0, 0, self.width, self.height), 2)
        pygame.draw.circle(self.image, BLACK, (8, 10), 2)
        pygame.draw.circle(self.image, BLACK, (22, 10), 2)

    def handle_input(self, keys):
        """Handle player movement input"""
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.move_speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.move_speed
            self.facing_right = True
        
        # Jump or wall jump
        jump_key = keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]
        if jump_key:
            if self.on_ground:
                self.vel_y = self.jump_power
                self.on_ground = False
            elif self.on_wall:
                # Wall jump - push away from wall
                self.vel_y = self.jump_power
                if self.wall_side == 'left':
                    self.vel_x = self.move_speed * 2  # Jump right
                else:
                    self.vel_x = -self.move_speed * 2  # Jump left
                self.on_wall = False
        
        # Attack key (X key or Ctrl)
        if keys[pygame.K_x] or keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            return True  # Signal that player is attacking
        return False

    def respawn(self, particles):
        """Respawn at checkpoint"""
        self.rect.x = self.checkpoint_x
        self.rect.y = self.checkpoint_y
        self.vel_x = 0
        self.vel_y = 0
        self.health = 100
        
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            particles.append(Particle(self.rect.centerx, self.rect.centery, CYAN, vel_x, vel_y, 40))

    def set_checkpoint(self, x, y, particles):
        """Set new checkpoint"""
        self.checkpoint_x = x
        self.checkpoint_y = y
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            particles.append(Particle(x, y, CYAN, vel_x, vel_y, 30))

    def update(self, platforms, spikes, coins, collectibles, goal, particles):
        """Update player physics and collisions"""
        self.vel_y += self.gravity
        if self.vel_y > 20:
            self.vel_y = 20

        # Store old position for better collision detection
        old_x = self.rect.x
        old_y = self.rect.y
        
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LEVEL_WIDTH:
            self.rect.right = LEVEL_WIDTH

        self.on_ground = False
        self.on_wall = False
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Ground collision - player falling onto platform
                if self.vel_y > 0 and old_y + self.height <= platform.rect.top + 5:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                # Ceiling collision - player jumping into platform
                elif self.vel_y < 0 and old_y >= platform.rect.bottom - 5:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
                # Wall collision (left side)
                elif self.vel_x < 0 and old_x + self.width <= platform.rect.right + 5:
                    self.rect.left = platform.rect.right
                    self.on_wall = True
                    self.wall_side = 'left'
                    self.vel_y *= 0.9  # Slow fall on wall
                # Wall collision (right side)
                elif self.vel_x > 0 and old_x >= platform.rect.left - 5:
                    self.rect.right = platform.rect.left
                    self.on_wall = True
                    self.wall_side = 'right'
                    self.vel_y *= 0.9  # Slow fall on wall

        for spike in spikes:
            if self.rect.colliderect(spike.rect):
                self.health -= 1
                if self.health <= 0:
                    return "dead"

        for coin in coins[:]:
            if self.rect.colliderect(coin.rect):
                self.coins += 1
                self.score += 10
                coins.remove(coin)
                for _ in range(8):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 4)
                    vel_x = math.cos(angle) * speed
                    vel_y = math.sin(angle) * speed
                    particles.append(Particle(coin.rect.centerx, coin.rect.centery, YELLOW, vel_x, vel_y, 20))

        for collectible in collectibles[:]:
            if self.rect.colliderect(collectible.rect):
                self.crystals += 1
                self.score += 25
                collectibles.remove(collectible)
                for _ in range(12):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 5)
                    vel_x = math.cos(angle) * speed
                    vel_y = math.sin(angle) * speed
                    particles.append(Particle(collectible.rect.centerx, collectible.rect.centery, PURPLE, vel_x, vel_y, 25))

        if self.rect.colliderect(goal.rect):
            self.score += 100
            return "goal"

        if self.rect.top > SCREEN_HEIGHT + 200:
            return "dead"

        self.draw_player()
        return None

# ============ PLATFORM CLASS ============
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=GREEN, moving=False, move_range=0):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.color = color
        self.moving = moving
        self.move_range = move_range
        self.move_direction = 1
        self.original_x = x
        self.draw_platform()

    def draw_platform(self):
        """Draw platform"""
        self.image.fill(self.color)
        pygame.draw.rect(self.image, WHITE, (0, 0, self.width, self.height), 2)

    def update(self):
        """Update platform position if moving"""
        if self.moving:
            self.rect.x += self.move_direction * 2
            if abs(self.rect.x - self.original_x) > self.move_range:
                self.move_direction *= -1

# ============ SPIKE CLASS ============
class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 20
        self.height = 25
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.draw_spike()

    def draw_spike(self):
        """Draw spike triangle"""
        points = [(self.width // 2, 0), (self.width, self.height), (0, self.height)]
        pygame.draw.polygon(self.image, RED, points)

# ============ COIN CLASS ============
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 15
        self.height = 15
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(center=(x, y))
        self.bob_offset = 0
        self.original_y = y
        self.draw_coin()

    def draw_coin(self):
        """Draw coin"""
        self.image.fill(DARK_BLUE)
        pygame.draw.circle(self.image, YELLOW, (self.width // 2, self.height // 2), 7)
        pygame.draw.circle(self.image, ORANGE, (self.width // 2, self.height // 2), 5)

    def update(self):
        """Make coin bob up and down"""
        self.bob_offset += 0.1
        self.rect.y = self.original_y + math.sin(self.bob_offset) * 5

# ============ COLLECTIBLE CLASS ============
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 20
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(center=(x, y))
        self.spin_angle = 0
        self.original_y = y
        self.draw_collectible()

    def draw_collectible(self):
        """Draw crystal collectible"""
        self.image.fill(DARK_BLUE)
        pygame.draw.polygon(self.image, PURPLE, [
            (10, 0), (20, 5), (15, 15), (10, 20), (5, 15), (0, 5)
        ])

    def update(self):
        """Make collectible spin and bob"""
        self.spin_angle += 3
        self.rect.y = self.original_y + math.sin(self.spin_angle * 0.1) * 5

# ============ ENEMY CLASS ============
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_range=100):
        super().__init__()
        self.width = 25
        self.height = 25
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.vel_x = 2
        self.patrol_range = patrol_range
        self.original_x = x
        self.health = 2  # Can be damaged twice
        self.alive = True
        self.attack_cooldown = 0
        self.attack_range = 80
        self.draw_enemy()

    def draw_enemy(self):
        """Draw enemy"""
        if self.alive:
            self.image.fill(RED)
            pygame.draw.rect(self.image, DARK_BLUE, (0, 0, self.width, self.height), 2)
            pygame.draw.circle(self.image, WHITE, (7, 8), 2)
            pygame.draw.circle(self.image, WHITE, (18, 8), 2)
            pygame.draw.circle(self.image, BLACK, (7, 8), 1)
            pygame.draw.circle(self.image, BLACK, (18, 8), 1)
            # Draw fangs when attacking
            if self.attack_cooldown > 0:
                pygame.draw.polygon(self.image, ORANGE, [(8, 15), (10, 20), (12, 15)])
                pygame.draw.polygon(self.image, ORANGE, [(15, 15), (17, 20), (19, 15)])

    def update(self):
        """Patrol back and forth"""
        if self.alive:
            self.rect.x += self.vel_x
            
            if abs(self.rect.x - self.original_x) > self.patrol_range:
                self.vel_x *= -1
            
            # Cooldown for attacks
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1

    def attack(self):
        """Prepare to attack"""
        self.attack_cooldown = 10
        self.draw_enemy()

    def take_damage(self, damage=1):
        """Enemy takes damage"""
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False

    def kill_enemy(self, particles):
        """Kill enemy with particle effect"""
        self.alive = False
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            particles.append(Particle(self.rect.centerx, self.rect.centery, RED, vel_x, vel_y, 30))

# ============ GOAL CLASS ============
class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 35
        self.height = 35
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(center=(x, y))
        self.rotation = 0
        self.draw_goal()

    def draw_goal(self):
        """Draw goal star"""
        self.image.fill(DARK_BLUE)
        pygame.draw.circle(self.image, YELLOW, (self.width // 2, self.height // 2), 15)
        pygame.draw.polygon(self.image, ORANGE, [
            (self.width // 2, 5), (self.width - 5, self.height - 8),
            (8, 12), (self.width - 8, 12), (5, self.height - 8)
        ])

    def update(self):
        """Make goal rotate"""
        self.rotation = (self.rotation + 2) % 360

# ============ LEVEL CLASS ============
class Level:
    def __init__(self, level_num):
        self.level_num = level_num
        self.camera_x = 0
        self.player = Player(100, 600)
        self.platforms = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.coins = []
        self.collectibles = []
        self.enemies = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()
        self.goal = None
        self.particles = []
        self.sounds_enabled = True
        
        # Set level theme
        self.theme = LEVEL_THEMES.get(level_num, LEVEL_THEMES[1])
        self.background_color = self.theme['bg']
        
        self.load_sounds()
        self.generate_level()

    def load_sounds(self):
        """Load sound effects"""
        try:
            self.jump_sound = pygame.mixer.Sound(JUMP_SOUND)
            self.coin_sound = pygame.mixer.Sound(COIN_SOUND)
            self.enemy_kill_sound = pygame.mixer.Sound(ENEMY_KILL_SOUND)
            self.jump_sound.set_volume(0.3)
            self.coin_sound.set_volume(0.2)
            self.enemy_kill_sound.set_volume(0.4)
        except Exception as e:
            print(f"Error loading sounds: {e}")
            self.sounds_enabled = False

    def generate_level(self):
        """Generate extended levels with checkpoints and themes"""
        platform_color = self.theme['platform']
        platform_light = self.theme['platform_light']
        
        if self.level_num == 1:
            # Beginner level - Grass Fields with wall jump intro
            self.platforms.add(Platform(0, 650, 250, 50, platform_color))
            self.platforms.add(Platform(350, 550, 150, 40, platform_color))
            self.platforms.add(Platform(600, 450, 150, 40, platform_color))
            self.platforms.add(Platform(850, 350, 150, 40, platform_color))
            self.platforms.add(Platform(1100, 450, 150, 40, platform_color))
            self.platforms.add(Platform(1350, 550, 150, 40, platform_color))
            self.platforms.add(Platform(1600, 400, 150, 40, platform_color))
            self.platforms.add(Platform(1850, 500, 150, 40, platform_color))
            self.platforms.add(Platform(2100, 350, 200, 40, platform_color))
            self.platforms.add(Platform(2400, 450, 150, 40, platform_color))
            self.platforms.add(Platform(2650, 550, 150, 40, platform_color))
            self.platforms.add(Platform(2900, 400, 300, 40, platform_color))
            
            # Add narrow passages for wall jumping
            self.platforms.add(Platform(500, 350, 40, 200, platform_light))  # Left wall
            self.platforms.add(Platform(560, 350, 40, 200, platform_light))  # Right wall
            
            # Checkpoints
            self.checkpoints.add(Checkpoint(425, 500, 1))
            self.checkpoints.add(Checkpoint(1425, 500, 2))
            self.checkpoints.add(Checkpoint(2475, 400, 3))
            
            # Coins
            for x in [425, 675, 925, 1175, 1425, 1675, 1925, 2175, 2475, 2725, 2975]:
                self.coins.append(Coin(x, 380))
            
            # Collectibles
            for x in [600, 1350, 2100, 2650]:
                self.collectibles.append(Collectible(x, 320))
            
            # Enemies
            self.enemies.add(Enemy(450, 600, 80))
            self.enemies.add(Enemy(1200, 500, 80))
            self.enemies.add(Enemy(2000, 600, 80))
            
            self.goal = Goal(2975, 300)

        elif self.level_num == 2:
            # Intermediate level - Desert Wastes with wall jumping challenges
            self.platforms.add(Platform(0, 650, 200, 50, platform_color))
            self.platforms.add(Platform(250, 550, 130, 40, platform_light, moving=True, move_range=80))
            self.platforms.add(Platform(500, 450, 130, 40, platform_color))
            
            # Wall jump section
            self.platforms.add(Platform(750, 300, 40, 250, platform_light))  # Left wall
            self.platforms.add(Platform(880, 300, 40, 250, platform_light))  # Right wall
            self.platforms.add(Platform(1000, 400, 130, 40, platform_color))
            
            self.platforms.add(Platform(1250, 450, 130, 40, platform_light, moving=True, move_range=80))
            self.platforms.add(Platform(1500, 350, 130, 40, platform_color))
            
            # Complex platforming section
            self.platforms.add(Platform(1750, 500, 100, 40, platform_color))
            self.platforms.add(Platform(1900, 450, 100, 40, platform_color))
            self.platforms.add(Platform(2050, 400, 100, 40, platform_color))
            self.platforms.add(Platform(2200, 350, 100, 40, platform_color))
            
            self.platforms.add(Platform(2350, 450, 130, 40, platform_light, moving=True, move_range=100))
            self.platforms.add(Platform(2600, 550, 200, 40, platform_color))
            self.platforms.add(Platform(2900, 400, 300, 40, platform_color))
            
            # Spikes around wall sections
            for y in [550, 600]:
                self.spikes.add(Spike(700, y))
                self.spikes.add(Spike(920, y))
            
            for x in [1700, 1850, 2000, 2150, 2550]:
                self.spikes.add(Spike(x, 600))
            
            # Checkpoints
            self.checkpoints.add(Checkpoint(575, 400, 1))
            self.checkpoints.add(Checkpoint(1200, 350, 2))
            self.checkpoints.add(Checkpoint(1900, 300, 3))
            self.checkpoints.add(Checkpoint(2700, 500, 4))
            
            # Coins
            for x in [325, 575, 825, 1075, 1325, 1575, 1825, 2075, 2325, 2575, 2825, 3100]:
                self.coins.append(Coin(x, 280))
            
            # Collectibles
            for x in [750, 1500, 2200, 3000]:
                self.collectibles.append(Collectible(x, 300))
            
            # More enemies to jump on
            self.enemies.add(Enemy(300, 500, 80))
            self.enemies.add(Enemy(900, 350, 80))
            self.enemies.add(Enemy(1400, 350, 80))
            self.enemies.add(Enemy(2000, 300, 80))
            self.enemies.add(Enemy(2700, 500, 80))
            
            self.goal = Goal(3000, 300)

        elif self.level_num == 3:
            # Expert level - Crystal Chamber
            self.platforms.add(Platform(0, 650, 180, 50, platform_color))
            self.platforms.add(Platform(200, 550, 100, 40, platform_light, moving=True, move_range=60))
            self.platforms.add(Platform(400, 450, 100, 40, platform_color))
            
            # First wall jump challenge
            self.platforms.add(Platform(600, 250, 40, 300, platform_light))  # Left wall
            self.platforms.add(Platform(740, 250, 40, 300, platform_light))  # Right wall
            self.platforms.add(Platform(850, 380, 100, 40, platform_color))
            
            self.platforms.add(Platform(1000, 480, 100, 40, platform_light, moving=True, move_range=100))
            self.platforms.add(Platform(1200, 380, 100, 40, platform_color))
            
            # Second wall jump section with moving walls
            self.platforms.add(Platform(1400, 300, 40, 250, platform_light, moving=True, move_range=50))
            self.platforms.add(Platform(1540, 300, 40, 250, platform_light, moving=True, move_range=50))
            self.platforms.add(Platform(1650, 380, 100, 40, platform_color))
            
            self.platforms.add(Platform(1800, 480, 100, 40, platform_light, moving=True, move_range=80))
            self.platforms.add(Platform(2000, 350, 100, 40, platform_color))
            
            # Final jumping section
            self.platforms.add(Platform(2200, 500, 80, 40, platform_color))
            self.platforms.add(Platform(2320, 450, 80, 40, platform_color))
            self.platforms.add(Platform(2440, 400, 80, 40, platform_color))
            self.platforms.add(Platform(2560, 350, 80, 40, platform_color))
            self.platforms.add(Platform(2680, 300, 80, 40, platform_color))
            
            self.platforms.add(Platform(2800, 500, 100, 40, platform_light, moving=True, move_range=100))
            self.platforms.add(Platform(3050, 400, 350, 40, platform_color))
            
            # Spikes in dangerous areas
            for x in [550, 790, 1350, 1580, 2150, 2270, 2390, 2510, 2630, 2750]:
                self.spikes.add(Spike(x, 600))
            
            # Checkpoints
            self.checkpoints.add(Checkpoint(300, 450, 1))
            self.checkpoints.add(Checkpoint(850, 330, 2))
            self.checkpoints.add(Checkpoint(1650, 330, 3))
            self.checkpoints.add(Checkpoint(2450, 300, 4))
            self.checkpoints.add(Checkpoint(2900, 450, 5))
            
            # Coins
            for x in [250, 450, 750, 1000, 1200, 1650, 1800, 2200, 2350, 2500, 2650, 2800, 3150]:
                self.coins.append(Coin(x, 280))
            
            # Collectibles scattered
            for x in [600, 1400, 2000, 2700, 3200]:
                self.collectibles.append(Collectible(x, 300))
            
            # Many enemies to jump on
            self.enemies.add(Enemy(250, 500, 60))
            self.enemies.add(Enemy(700, 300, 60))
            self.enemies.add(Enemy(1050, 400, 60))
            self.enemies.add(Enemy(1450, 300, 60))
            self.enemies.add(Enemy(1850, 420, 60))
            self.enemies.add(Enemy(2300, 420, 60))
            self.enemies.add(Enemy(2700, 480, 60))
            
            self.goal = Goal(3200, 300)

    def update_camera(self):
        """Update camera position to follow player"""
        target_camera_x = max(0, self.player.rect.centerx - SCREEN_WIDTH // 3)
        target_camera_x = min(target_camera_x, LEVEL_WIDTH - SCREEN_WIDTH)
        self.camera_x += (target_camera_x - self.camera_x) * 0.1

    def get_screen_rect(self, rect):
        """Convert world rect to screen rect based on camera position"""
        screen_rect = rect.copy()
        screen_rect.x -= self.camera_x
        return screen_rect

    def draw(self, screen, font):
        """Draw level"""
        screen.fill(self.background_color)
        
        for platform in self.platforms:
            screen_rect = self.get_screen_rect(platform.rect)
            if -100 < screen_rect.x < SCREEN_WIDTH + 100:
                screen.blit(platform.image, screen_rect)
        
        for spike in self.spikes:
            screen_rect = self.get_screen_rect(spike.rect)
            if -100 < screen_rect.x < SCREEN_WIDTH + 100:
                screen.blit(spike.image, screen_rect)
        
        for coin in self.coins:
            screen_rect = self.get_screen_rect(coin.rect)
            if -100 < screen_rect.x < SCREEN_WIDTH + 100:
                screen.blit(coin.image, screen_rect)
        
        for collectible in self.collectibles:
            screen_rect = self.get_screen_rect(collectible.rect)
            if -100 < screen_rect.x < SCREEN_WIDTH + 100:
                screen.blit(collectible.image, screen_rect)
        
        for enemy in self.enemies:
            if enemy.alive:  # Only draw alive enemies
                screen_rect = self.get_screen_rect(enemy.rect)
                if -100 < screen_rect.x < SCREEN_WIDTH + 100:
                    screen.blit(enemy.image, screen_rect)
        
        for checkpoint in self.checkpoints:
            screen_rect = self.get_screen_rect(checkpoint.rect)
            if -100 < screen_rect.x < SCREEN_WIDTH + 100:
                screen.blit(checkpoint.image, screen_rect)
        
        screen_rect = self.get_screen_rect(self.goal.rect)
        if -100 < screen_rect.x < SCREEN_WIDTH + 100:
            screen.blit(self.goal.image, screen_rect)
        
        screen_rect = self.get_screen_rect(self.player.rect)
        screen.blit(self.player.image, screen_rect)
        
        # Draw particles
        for particle in self.particles[:]:
            screen_rect = self.get_screen_rect(particle.rect)
            if -100 < screen_rect.x < SCREEN_WIDTH + 100:
                screen.blit(particle.image, screen_rect)
        
        # HUD
        level_text = font.render(f"Level {self.level_num}", True, WHITE)
        health_text = font.render(f"Health: {max(0, self.player.health)}", True, RED)
        coins_text = font.render(f"Coins: {self.player.coins}", True, YELLOW)
        crystals_text = font.render(f"Crystals: {self.player.crystals}", True, PURPLE)
        score_text = font.render(f"Score: {self.player.score}", True, CYAN)
        progress_text = font.render(f"Progress: {int((self.player.rect.x / LEVEL_WIDTH) * 100)}%", True, LIGHT_BLUE)
        
        screen.blit(level_text, (10, 10))
        screen.blit(health_text, (10, 40))
        screen.blit(coins_text, (10, 70))
        screen.blit(crystals_text, (10, 100))
        screen.blit(score_text, (10, 130))
        screen.blit(progress_text, (SCREEN_WIDTH - 250, 10))

    def run(self, screen, clock, font):
        """Main game loop for level"""
        running = True
        while running and self.player.alive:
            clock.tick(FPS)
            
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None

            # Track old state for sound effects
            old_coins = self.player.coins
            old_crystals = self.player.crystals
            old_vel_y = self.player.vel_y
            old_on_ground = self.player.on_ground
            
            attacking = self.player.handle_input(keys)
            
            self.platforms.update()
            self.enemies.update()
            for coin in self.coins:
                coin.update()
            for collectible in self.collectibles:
                collectible.update()
            
            # Handle player attacking enemies
            if attacking:
                for enemy in self.enemies:
                    if enemy.alive:
                        # Check if enemy is in attack range (close to player)
                        dist = math.sqrt((enemy.rect.centerx - self.player.rect.centerx)**2 + 
                                        (enemy.rect.centery - self.player.rect.centery)**2)
                        if dist < 60:  # Attack range
                            if enemy.take_damage(1):  # Remove 1 health
                                enemy.kill_enemy(self.particles)
                                self.player.score += 50
                                if self.sounds_enabled:
                                    self.enemy_kill_sound.play()
                            else:
                                enemy.attack()
            
            # Check enemy collisions
            for enemy in self.enemies:
                if enemy.alive and self.player.rect.colliderect(enemy.rect):
                    # Jump on enemy to kill it
                    if self.player.vel_y > 0 and self.player.rect.bottom - self.player.vel_y <= enemy.rect.top:
                        enemy.kill_enemy(self.particles)
                        self.player.vel_y = self.player.jump_power  # Bounce off
                        self.player.score += 50
                        if self.sounds_enabled:
                            self.enemy_kill_sound.play()
                    # Hit from side - take damage
                    elif enemy.alive:
                        self.player.health -= 2
                        if self.player.health <= 0:
                            self.player.alive = False
            
            # Check checkpoint collisions
            for checkpoint in self.checkpoints:
                if self.player.rect.colliderect(checkpoint.rect) and not checkpoint.activated:
                    checkpoint.activate()
                    self.player.set_checkpoint(checkpoint.rect.centerx, checkpoint.rect.centery, self.particles)
            
            self.update_camera()
            
            result = self.player.update(self.platforms, self.spikes, self.coins, self.collectibles, self.goal, self.particles)
            
            if result == "dead":
                self.player.respawn(self.particles)
                self.player.alive = True
            elif result == "goal":
                return True
            
            # Play sounds for collected items
            if self.player.coins > old_coins and self.sounds_enabled:
                self.coin_sound.play()
            if self.player.crystals > old_crystals and self.sounds_enabled:
                self.coin_sound.play()
            
            # Play jump sound
            if self.player.on_ground and old_vel_y > 0 and self.player.vel_y < 0 and self.sounds_enabled:
                self.jump_sound.play()
            
            # Update particles
            for particle in self.particles[:]:
                particle.update()
                if particle.lifetime <= 0:
                    self.particles.remove(particle)
            
            self.draw(screen, font)
            pygame.display.flip()

        return False

def show_level_complete_menu(screen, clock, font, big_font, level_num, level_stats):
    """Show level complete screen with replay/next options"""
    selecting = True
    selected = 0
    options = ["Next Level", "Replay Level", "Return to Menu"]
    
    while selecting:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if selected == 0:
                        return "next"
                    elif selected == 1:
                        return "replay"
                    elif selected == 2:
                        return "menu"
        
        screen.fill(DARK_BLUE)
        
        title = big_font.render(f"Level {level_num} Complete!", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        stats_text = font.render(
            f"Crystals: +{level_stats['crystals']} | Coins: +{level_stats['coins']} | Score: {level_stats['score']}", 
            True, PURPLE
        )
        screen.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, 150))
        
        # Draw options
        for i, option in enumerate(options):
            if i == selected:
                option_text = font.render(f"> {option} <", True, YELLOW)
            else:
                option_text = font.render(option, True, WHITE)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, 300 + i * 80))
        
        hint = font.render("Use UP/DOWN to select, ENTER to confirm", True, GRAY)
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 650))
        
        pygame.display.flip()

# ============ MAIN MENU ============
def show_menu(screen, clock, font, big_font, player_stats):
    """Display main menu"""
    running = True
    while running:
        clock.tick(FPS)
        
        screen.fill(DARK_BLUE)
        
        title = big_font.render("QUEST MADNESS", True, YELLOW)
        subtitle = font.render("A Platforming Adventure", True, LIGHT_BLUE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 170))
        
        options = [
            "1. Start Game",
            "2. Replay Levels",
            "3. Shop",
            "4. Tutorial",
            "5. Exit"
        ]
        
        for i, option in enumerate(options):
            text = font.render(option, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 300 + i * 60))
        
        stats_text = font.render(f"Total Crystals: {player_stats['crystals']} | Total Coins: {player_stats['coins']}", True, PURPLE)
        screen.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, SCREEN_HEIGHT - 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "start"
                elif event.key == pygame.K_2:
                    return "replay"
                elif event.key == pygame.K_3:
                    return "shop"
                elif event.key == pygame.K_4:
                    return "tutorial"
                elif event.key == pygame.K_5:
                    return "quit"

def show_shop(screen, clock, font, big_font, player_stats):
    """Display shop menu"""
    running = True
    selected = 0
    shop_items = [
        {"name": "Health Potion", "cost": 5, "effect": "health"},
        {"name": "Speed Boost", "cost": 10, "effect": "speed"},
        {"name": "Extra Lives", "cost": 15, "effect": "lives"},
        {"name": "Go Back", "cost": 0, "effect": "back"},
    ]
    
    while running:
        clock.tick(FPS)
        
        screen.fill(DARK_BLUE)
        
        title = big_font.render("SHOP", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        stats = font.render(f"Crystals: {player_stats['crystals']} | Coins: {player_stats['coins']}", True, PURPLE)
        screen.blit(stats, (SCREEN_WIDTH // 2 - stats.get_width() // 2, 130))
        
        for i, item in enumerate(shop_items):
            if i == selected:
                color = YELLOW
                prefix = "> "
            else:
                color = WHITE
                prefix = "  "
            
            if item["effect"] != "back":
                text = font.render(f"{prefix}{item['name']} - {item['cost']} Crystals", True, color)
            else:
                text = font.render(f"{prefix}{item['name']}", True, color)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 220 + i * 70))
        
        instructions = font.render("Use [UP/DOWN] to select, [ENTER] to buy, [ESC] to exit", True, LIGHT_BLUE)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return player_stats
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(shop_items)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(shop_items)
                elif event.key == pygame.K_RETURN:
                    item = shop_items[selected]
                    if item["effect"] == "back":
                        return player_stats
                    elif player_stats["crystals"] >= item["cost"]:
                        player_stats["crystals"] -= item["cost"]
                        if item["effect"] == "health":
                            player_stats["max_health"] += 25
                        elif item["effect"] == "speed":
                            player_stats["speed_bonus"] += 1
                        elif item["effect"] == "lives":
                            player_stats["lives"] += 1
                elif event.key == pygame.K_ESCAPE:
                    return player_stats

def show_tutorial(screen, clock, font):
    """Display tutorial"""
    running = True
    while running:
        clock.tick(FPS)
        
        screen.fill(DARK_BLUE)
        
        title = font.render("TUTORIAL", True, YELLOW)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        tutorial_text = [
            "CONTROLS:",
            "[A/D] or [LEFT/RIGHT] - Move",
            "[W] or [SPACE] or [UP] - Jump / Wall Jump",
            "[X] or [CTRL] - Attack enemies",
            "[ESC] - Quit to Menu",
            "",
            "GAME OBJECTS:",
            "YELLOW SQUARE = You (the player)",
            "GREEN/TAN/BLUE = Platforms (walk on these)",
            "MOVING PLATFORMS = Platforms that move back & forth",
            "CYAN FLAG = Checkpoints (respawn here)",
            "YELLOW = Coins (collect for 10 points)",
            "PURPLE = Crystals (spend in shop for 25 points)",
            "RED SQUARE = Enemies (jump on or attack to kill!)",
            "UPWARD TRIANGLE = Spikes (avoid or die!)",
            "YELLOW STAR = Goal (reach to complete level)",
            "",
            "ADVANCED MECHANICS:",
            "WALL JUMPING: Jump near walls to slide & jump off with momentum",
            "ENEMY KILLING: Jump on top OR attack with [X] to defeat enemies",
            "ATTACKING: Press [X] near enemies to attack (costs stamina)",
            "CHECKPOINT RESPAWNING: Activate checkpoints, respawn there when dying",
            "",
            "GAME FEATURES:",
            "INFINITE LIVES: You have unlimited respawns!",
            "PROGRESS SAVED: Your stats are automatically saved",
            "3 THEMED LEVELS: Grass Fields → Desert → Crystal Chamber",
            "",
            "SCORING:",
            "Coins: 10 pts | Crystals: 25 pts | Enemy Kill: 50 pts | Goal: 100 pts",
            "",
            "Press any key to return to menu"
        ]
        
        for i, line in enumerate(tutorial_text):
            if line:
                text = font.render(line, True, WHITE)
            else:
                text = font.render("", True, WHITE)
            screen.blit(text, (30, 130 + i * 20))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                return "menu"

def main():
    """Main game loop"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Quest Madness")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)
    
    # Initialize background music
    try:
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Loop music indefinitely
        music_enabled = True
    except Exception as e:
        print(f"Error loading music: {e}")
        music_enabled = False
    
    # Load saved progress or start fresh
    player_stats = load_progress()
    
    level_num = 1
    max_levels = 3
    
    while True:
        choice = show_menu(screen, clock, font, big_font, player_stats)
        
        if choice == "quit" or choice is None:
            # Save progress before quitting
            save_progress(player_stats)
            break
        elif choice == "shop":
            player_stats = show_shop(screen, clock, font, big_font, player_stats)
            save_progress(player_stats)  # Save after shop purchases
        elif choice == "tutorial":
            show_tutorial(screen, clock, font)
        elif choice == "replay":
            # Replay all levels from level 1
            level_num = 1
            while level_num <= max_levels:
                level = Level(level_num)
                level.player.health = player_stats['max_health']
                result = level.run(screen, clock, font)
                
                if result is None:
                    break
                elif result:
                    # Show level complete menu with replay option
                    level_stats = {
                        'crystals': level.player.crystals,
                        'coins': level.player.coins,
                        'score': level.player.score
                    }
                    menu_choice = show_level_complete_menu(screen, clock, font, big_font, level_num, level_stats)
                    
                    if menu_choice == "next":
                        level_num += 1
                    elif menu_choice == "replay":
                        # Stay on same level
                        continue
                    elif menu_choice == "menu" or menu_choice is None:
                        break
                else:
                    screen.fill(RED)
                    text = big_font.render("Game Over!", True, YELLOW)
                    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    break
            
            if level_num > max_levels:
                screen.fill(DARK_BLUE)
                text = big_font.render("Replay Complete!", True, YELLOW)
                subtext = font.render("You finished replaying all levels!", True, LIGHT_BLUE)
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
                screen.blit(subtext, (SCREEN_WIDTH // 2 - subtext.get_width() // 2, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000)
        elif choice == "start":
            level_num = player_stats.get('highest_level', 1)
            while level_num <= max_levels:
                level = Level(level_num)
                level.player.health = player_stats['max_health']
                result = level.run(screen, clock, font)
                
                if result is None:
                    break
                elif result:
                    player_stats['crystals'] += level.player.crystals
                    player_stats['coins'] += level.player.coins
                    # Update highest level reached
                    if level_num >= player_stats.get('highest_level', 1):
                        player_stats['highest_level'] = level_num + 1
                    
                    # Show level complete menu with replay option
                    level_stats = {
                        'crystals': level.player.crystals,
                        'coins': level.player.coins,
                        'score': level.player.score
                    }
                    menu_choice = show_level_complete_menu(screen, clock, font, big_font, level_num, level_stats)
                    
                    if menu_choice == "next":
                        save_progress(player_stats)
                        level_num += 1
                    elif menu_choice == "replay":
                        # Reset player stats and replay current level
                        level_num = level_num  # Stay on same level
                        continue
                    elif menu_choice == "menu" or menu_choice is None:
                        save_progress(player_stats)
                        break
                else:
                    screen.fill(RED)
                    text = big_font.render("Game Over!", True, YELLOW)
                    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    # Save progress even on failure
                    save_progress(player_stats)
                    break
            
            if level_num > max_levels:
                screen.fill(DARK_BLUE)
                text = big_font.render("You Win!", True, YELLOW)
                subtext = font.render("You completed all levels!", True, LIGHT_BLUE)
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
                screen.blit(subtext, (SCREEN_WIDTH // 2 - subtext.get_width() // 2, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
