"""Player character class"""
import pygame
from constants import *
from weapons import get_weapon_surface

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon, health=100, color=BLUE):
        super().__init__()
        self.x = x
        self.y = y
        self.weapon = weapon
        self.health = health
        self.max_health = health
        self.color = color
        
        # Create sprite
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement
        self.vel_x = 0
        self.vel_y = 0
        self.is_jumping = False
        self.is_attacking = False
        self.attack_cooldown = 0
        
        # Facing direction (1 = right, -1 = left)
        self.facing = 1
        self.on_ground = True
    
    def handle_input(self, event):
        # This method is kept for compatibility but movement is now handled in game.py
        pass
    
    def update(self):
        # Apply gravity
        if not self.on_ground:
            self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Boundary collision (ground)
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.y = self.rect.y
            self.vel_y = 0
            self.on_ground = True
            self.is_jumping = False
        
        # Boundary collision (sides)
        if self.rect.left < 0:
            self.rect.left = 0
            self.x = self.rect.x
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.x = self.rect.x
        
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Draw weapon
        self.draw_weapon()
    
    def draw_weapon(self):
        """Draw weapon on the player"""
        # Fill body color (weapon will be drawn as overlay in game.draw)
        self.image.fill(self.color)

    def get_weapon_draw_info(self):
        """Return (surface, pygame.Rect, facing) for weapon overlay drawing.
        The surface is already colored; rect is in screen coordinates.
        """
        if self.weapon not in WEAPONS:
            return None

        weapon_info = WEAPONS[self.weapon]
        weapon_color = weapon_info.get("color", (200,200,200))

        # create weapon surface (cached inside weapons.get_weapon_surface)
        surf = get_weapon_surface(self.weapon, weapon_color, scale=2)

        # compute draw position so weapon appears near player's hand
        sx, sy = surf.get_size()
        weapon_y = self.rect.top + (PLAYER_HEIGHT // 2 - sy // 2)
        if self.facing == 1:
            weapon_x = self.rect.right - 8
        else:
            # when facing left, position to left side
            weapon_x = self.rect.left - sx + 8

        rect = pygame.Rect(int(weapon_x), int(weapon_y), sx, sy)
        return (surf, rect, self.facing)
    
    def get_weapon_damage(self):
        if self.weapon in WEAPONS:
            return WEAPONS[self.weapon]["damage"]
        return 10
    
    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
