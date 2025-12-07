"""Visual effects"""
import pygame
from constants import *

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage):
        super().__init__()
        self.x = x
        self.y = y
        self.damage = damage
        self.lifetime = 60  # frames
        
        # Create text surface
        font = pygame.font.Font(None, 36)
        self.image = font.render(str(damage), True, RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        self.lifetime -= 1
        # Float upward
        self.rect.y -= 2
        
        if self.lifetime <= 0:
            self.kill()
