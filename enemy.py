"""Enemy character class"""
import pygame
import random
from constants import *
from weapons import get_weapon_surface

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon, health=100, speed=5, ai_update_freq=30, damage_multiplier=1.0, color=RED):
        super().__init__()
        self.x = x
        self.y = y
        self.weapon = weapon
        self.health = health
        self.max_health = health
        self.speed = speed
        self.ai_update_freq = ai_update_freq
        self.damage_multiplier = damage_multiplier
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
        self.facing = -1
        self.on_ground = True
        
        # AI
        self.ai_counter = 0
        self.ai_decision = None
    
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
        
        # AI behavior
        self.update_ai()
        
        # Draw weapon
        self.draw_weapon()
    
    def update_ai(self):
        self.ai_counter += 1
        
        if self.ai_counter >= self.ai_update_freq:
            self.ai_counter = 0
            # Simple AI: randomly move towards player or attack
            action = random.choice(["attack", "move_left", "move_right", "jump"])
            
            if action == "attack":
                self.is_attacking = True
            elif action == "move_left":
                self.vel_x = self.speed
                self.facing = 1
            elif action == "move_right":
                self.vel_x = -self.speed
                self.facing = -1
            elif action == "jump" and self.on_ground:
                self.vel_y = -PLAYER_JUMP_POWER
                self.is_jumping = True
                self.on_ground = False
    
    def draw_weapon(self):
        """Draw weapon on the enemy"""
        # Fill body color (weapon overlay handled by Game.draw)
        self.image.fill(self.color)

    def get_weapon_draw_info(self):
        """Return (surface, pygame.Rect, facing) for enemy weapon overlay drawing."""
        if self.weapon not in WEAPONS:
            return None

        weapon_info = WEAPONS[self.weapon]
        weapon_color = weapon_info.get("color", (200,200,200))

        surf = get_weapon_surface(self.weapon, weapon_color, scale=2)
        sx, sy = surf.get_size()

        weapon_y = self.rect.top + (PLAYER_HEIGHT // 2 - sy // 2)
        if self.facing == 1:
            weapon_x = self.rect.right - 8
        else:
            weapon_x = self.rect.left - sx + 8

        rect = pygame.Rect(int(weapon_x), int(weapon_y), sx, sy)
        return (surf, rect, self.facing)
    
    def get_weapon_damage(self):
        if self.weapon in WEAPONS:
            base_damage = WEAPONS[self.weapon]["damage"]
            return int(base_damage * self.damage_multiplier)
        return int(10 * self.damage_multiplier)
    
    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
    
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
