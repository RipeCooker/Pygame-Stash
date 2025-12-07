"""Map/Arena class"""
import pygame
from constants import *

class Map:
    def __init__(self, map_name):
        self.map_name = map_name
        if map_name in MAPS:
            self.map_data = MAPS[map_name]
        else:
            self.map_data = MAPS["Arena"]
        
        self.bg_color = self.map_data["bg_color"]
        self.accent_color = self.map_data["accent_color"]
        self.display_name = self.map_data["name"]
    
    def draw(self, screen):
        """Draw the map background and decorations"""
        # Draw background
        screen.fill(self.bg_color)
        
        # Draw decorative elements based on map type
        if self.map_name == "Forest":
            self.draw_forest(screen)
        elif self.map_name == "Desert":
            self.draw_desert(screen)
        elif self.map_name == "Ice":
            self.draw_ice(screen)
        elif self.map_name == "Volcano":
            self.draw_volcano(screen)
        elif self.map_name == "Castle":
            self.draw_castle(screen)
        else:
            self.draw_arena(screen)
        
        # Draw battle ground
        pygame.draw.line(screen, self.accent_color, (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 3)
    
    def draw_arena(self, screen):
        """Draw dark arena"""
        # Draw corner decorations
        pygame.draw.circle(screen, self.accent_color, (50, 50), 20)
        pygame.draw.circle(screen, self.accent_color, (SCREEN_WIDTH - 50, 50), 20)
        pygame.draw.circle(screen, self.accent_color, (50, SCREEN_HEIGHT - 100), 20)
        pygame.draw.circle(screen, self.accent_color, (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 100), 20)
    
    def draw_forest(self, screen):
        """Draw forest scene"""
        # Draw trees (simple rectangles)
        tree_positions = [(100, 100), (300, 150), (600, 80), (900, 120), (1100, 100)]
        for x, y in tree_positions:
            pygame.draw.rect(screen, (50, 100, 30), (x - 20, y - 30, 40, 60))
            pygame.draw.circle(screen, (100, 200, 50), (x, y - 40), 40)
    
    def draw_desert(self, screen):
        """Draw desert scene"""
        # Draw sand dunes
        for i in range(3):
            x = i * 400
            pygame.draw.polygon(screen, (240, 200, 80), [(x, 200), (x + 200, 100), (x + 400, 200)])
    
    def draw_ice(self, screen):
        """Draw ice scene"""
        # Draw ice blocks
        for i in range(0, SCREEN_WIDTH, 150):
            for j in range(0, SCREEN_HEIGHT - 100, 150):
                pygame.draw.rect(screen, (200, 230, 255), (i, j, 100, 100), 2)
    
    def draw_volcano(self, screen):
        """Draw volcano scene"""
        # Draw lava at bottom
        pygame.draw.polygon(screen, (200, 50, 0), [(0, SCREEN_HEIGHT - 100), (SCREEN_WIDTH, SCREEN_HEIGHT - 100), 
                                                     (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)])
        # Draw volcano peak
        pygame.draw.polygon(screen, (100, 30, 10), [(SCREEN_WIDTH // 2 - 150, 300), 
                                                      (SCREEN_WIDTH // 2 + 150, 300), 
                                                      (SCREEN_WIDTH // 2, 100)])
    
    def draw_castle(self, screen):
        """Draw castle scene"""
        # Draw castle walls
        pygame.draw.rect(screen, (100, 100, 120), (100, 150, 400, 250))
        pygame.draw.rect(screen, (100, 100, 120), (SCREEN_WIDTH - 500, 150, 400, 250))
        
        # Draw towers
        pygame.draw.rect(screen, (80, 80, 100), (150, 100, 80, 300))
        pygame.draw.rect(screen, (80, 80, 100), (SCREEN_WIDTH - 230, 100, 80, 300))
