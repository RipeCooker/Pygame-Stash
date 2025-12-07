"""UI management"""
import pygame
from constants import *

class UIManager:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.game_over_winner = None
    
    def draw_menu(self, screen):
        """Draw main menu"""
        screen.fill(BG_COLOR)
        
        # Title
        title = self.font_large.render("Ultimate Rumble", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_small.render("A 2D Fighting Game", True, GRAY)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 160))
        screen.blit(subtitle, subtitle_rect)
        
        # Menu options
        option1 = self.font_medium.render("1. Start Game", True, WHITE)
        option1_rect = option1.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(option1, option1_rect)
        
        option2 = self.font_medium.render("2. Options", True, WHITE)
        option2_rect = option2.get_rect(center=(SCREEN_WIDTH // 2, 350))
        screen.blit(option2, option2_rect)
        
        option3 = self.font_medium.render("3. Exit", True, WHITE)
        option3_rect = option3.get_rect(center=(SCREEN_WIDTH // 2, 450))
        screen.blit(option3, option3_rect)
        
        # Instructions
        instructions = self.font_small.render("Press the corresponding number to select", True, GRAY)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 600))
        screen.blit(instructions, instructions_rect)
    
    def draw_mode_select(self, screen):
        """Draw game mode selection screen"""
        screen.fill(BG_COLOR)
        
        # Title
        title = self.font_large.render("Select Game Mode", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Mode options
        mode1 = self.font_medium.render("1. Story Mode (Campaign)", True, BLUE)
        mode1_rect = mode1.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(mode1, mode1_rect)
        
        mode2 = self.font_medium.render("2. Endless Mode (Survive)", True, GREEN)
        mode2_rect = mode2.get_rect(center=(SCREEN_WIDTH // 2, 350))
        screen.blit(mode2, mode2_rect)
        
        mode3 = self.font_medium.render("3. Rumble Mode (No Damage)", True, ORANGE)
        mode3_rect = mode3.get_rect(center=(SCREEN_WIDTH // 2, 450))
        screen.blit(mode3, mode3_rect)
        
        # Back instruction
        back = self.font_small.render("Press ESC to go back", True, GRAY)
        back_rect = back.get_rect(center=(SCREEN_WIDTH // 2, 600))
        screen.blit(back, back_rect)
    
    def draw_difficulty_select(self, screen):
        """Draw difficulty selection screen"""
        screen.fill(BG_COLOR)
        
        # Title
        title = self.font_large.render("Select Difficulty", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title, title_rect)
        
        # Difficulty options
        diff1 = self.font_medium.render("1. Easy (Health: 150, Weak Enemy)", True, GREEN)
        diff1_rect = diff1.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(diff1, diff1_rect)
        
        diff2 = self.font_medium.render("2. Normal (Health: 100, Normal Enemy)", True, WHITE)
        diff2_rect = diff2.get_rect(center=(SCREEN_WIDTH // 2, 280))
        screen.blit(diff2, diff2_rect)
        
        diff3 = self.font_medium.render("3. Hard (Health: 80, Strong Enemy)", True, ORANGE)
        diff3_rect = diff3.get_rect(center=(SCREEN_WIDTH // 2, 360))
        screen.blit(diff3, diff3_rect)
        
        diff4 = self.font_medium.render("4. Insane (Health: 60, Very Strong)", True, RED)
        diff4_rect = diff4.get_rect(center=(SCREEN_WIDTH // 2, 440))
        screen.blit(diff4, diff4_rect)
        
        # Back instruction
        back = self.font_small.render("Press ESC to go back", True, GRAY)
        back_rect = back.get_rect(center=(SCREEN_WIDTH // 2, 600))
        screen.blit(back, back_rect)
    
    def draw_map_select(self, screen, map_list, selected_index):
        """Draw map selection screen"""
        screen.fill(BG_COLOR)
        
        # Title
        title = self.font_large.render("Select Your Map", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        # Display maps
        start_idx = max(0, selected_index - 2)
        end_idx = min(len(map_list), start_idx + 5)
        
        y_pos = 150
        for i in range(start_idx, end_idx):
            map_name = map_list[i]
            map_data = MAPS[map_name]
            display_name = map_data["name"]
            
            if i == selected_index:
                # Highlight selected map
                map_text = self.font_medium.render(f"→ {display_name} ←", True, GOLD)
                # Draw preview of map color
                pygame.draw.rect(screen, map_data["bg_color"], (SCREEN_WIDTH // 2 - 150, y_pos - 15, 300, 40))
            else:
                map_text = self.font_medium.render(display_name, True, WHITE)
            
            map_rect = map_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(map_text, map_rect)
            y_pos += 80
        
        # Instructions
        instructions = self.font_small.render("UP/DOWN: Navigate | ENTER: Select | ESC: Back", True, GRAY)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(instructions, instructions_rect)

    def draw_story(self, screen, speaker, text, title=None):
        """Draw a dialog box for story/cutscenes."""
        # Dim background slightly
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        # Dialog box
        box_w = SCREEN_WIDTH - 120
        box_h = 180
        box_x = 60
        box_y = SCREEN_HEIGHT - box_h - 40
        pygame.draw.rect(screen, (20, 20, 30), (box_x, box_y, box_w, box_h))
        pygame.draw.rect(screen, WHITE, (box_x, box_y, box_w, box_h), 2)

        # Title (optional)
        if title:
            title_surf = self.font_medium.render(title, True, YELLOW)
            screen.blit(title_surf, (box_x + 12, box_y + 8))

        # Speaker
        speaker_surf = self.font_small.render(f"{speaker}", True, GOLD)
        screen.blit(speaker_surf, (box_x + 12, box_y + 40))

        # Wrap text into lines
        max_w = box_w - 40
        words = text.split()
        lines = []
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            test_surf = self.font_small.render(test, True, WHITE)
            if test_surf.get_width() <= max_w:
                cur = test
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)

        # Render lines
        y = box_y + 70
        for line in lines[:4]:
            txt = self.font_small.render(line, True, WHITE)
            screen.blit(txt, (box_x + 12, y))
            y += 28

        # Continue hint
        hint = self.font_small.render("Press SPACE/ENTER to continue", True, GRAY)
        hint_rect = hint.get_rect(topright=(box_x + box_w - 12, box_y + box_h - 12))
        screen.blit(hint, hint_rect)
    
    def draw_weapon_select(self, screen, weapon_list, selected_index):
        """Draw weapon selection screen"""
        screen.fill(BG_COLOR)
        
        # Title
        title = self.font_large.render("Select Your Weapon", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        # Display weapons in a scrollable list
        start_idx = max(0, selected_index - 3)
        end_idx = min(len(weapon_list), start_idx + 7)
        
        y_pos = 150
        for i in range(start_idx, end_idx):
            weapon = weapon_list[i]
            damage = WEAPONS[weapon]["damage"]
            
            if i == selected_index:
                # Highlight selected weapon
                weapon_text = self.font_medium.render(f"→ {weapon.upper()} (Damage: {damage}) ←", True, GOLD)
            else:
                weapon_text = self.font_medium.render(f"{weapon.upper()} (Damage: {damage})", True, WHITE)
            
            weapon_rect = weapon_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(weapon_text, weapon_rect)
            y_pos += 60
        
        # Instructions
        instructions = self.font_small.render("UP/DOWN: Navigate | ENTER: Select | ESC: Back", True, GRAY)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(instructions, instructions_rect)
    
    def draw_color_select(self, screen, color_list, selected_index):
        """Draw color selection screen"""
        screen.fill(BG_COLOR)
        
        # Title
        title = self.font_large.render("Select Your Color", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        # Color names mapping
        color_names = ["Blue", "Cyan", "Purple", "Lime", "Magenta", "Teal"]
        
        # Display colors
        start_idx = max(0, selected_index - 2)
        end_idx = min(len(color_list), start_idx + 5)
        
        y_pos = 150
        for i in range(start_idx, end_idx):
            color = color_list[i]
            color_name = color_names[i]
            
            if i == selected_index:
                # Highlight selected color
                color_text = self.font_medium.render(f"→ {color_name} ←", True, color)
                # Draw a bigger preview rectangle for selected
                pygame.draw.rect(screen, color, (SCREEN_WIDTH // 2 - 50, y_pos - 15, 100, 30), 3)
            else:
                color_text = self.font_medium.render(color_name, True, WHITE)
            
            color_rect = color_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(color_text, color_rect)
            y_pos += 80
        
        # Instructions
        instructions = self.font_small.render("UP/DOWN: Navigate | ENTER: Select | ESC: Back", True, GRAY)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(instructions, instructions_rect)
    
    def draw_game_ui(self, screen, player, enemy, game_mode=None, difficulty=None, level=1, enemies_defeated=0, map_name=None):
        """Draw game UI elements"""
        # Player health bar
        self.draw_health_bar(screen, 20, 20, 200, 30, player.health, player.max_health, "Player")
        
        # Enemy health bar
        self.draw_health_bar(screen, SCREEN_WIDTH - 220, 20, 200, 30, enemy.health, enemy.max_health, "Enemy")
        
        # Player weapon info (larger and clearer)
        weapon_color = WEAPONS[player.weapon]["color"]
        player_weapon = self.font_medium.render(f"Weapon: {player.weapon.upper()}", True, weapon_color)
        screen.blit(player_weapon, (20, 65))
        
        # Player damage
        player_damage = self.font_small.render(f"Damage: {player.get_weapon_damage()}", True, weapon_color)
        screen.blit(player_damage, (20, 95))
        
        # Enemy weapon info (larger and clearer)
        enemy_weapon_color = WEAPONS[enemy.weapon]["color"]
        enemy_weapon = self.font_medium.render(f"Enemy: {enemy.weapon.upper()}", True, enemy_weapon_color)
        enemy_weapon_rect = enemy_weapon.get_rect(topright=(SCREEN_WIDTH - 20, 65))
        screen.blit(enemy_weapon, enemy_weapon_rect)
        
        # Enemy damage
        enemy_damage = self.font_small.render(f"Damage: {enemy.get_weapon_damage()}", True, enemy_weapon_color)
        enemy_damage_rect = enemy_damage.get_rect(topright=(SCREEN_WIDTH - 20, 95))
        screen.blit(enemy_damage, enemy_damage_rect)
        
        # Game mode and difficulty info
        if game_mode:
            mode_text = self.font_small.render(f"Mode: {game_mode} | Difficulty: {difficulty.upper()}", True, YELLOW)
            mode_rect = mode_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
            screen.blit(mode_text, mode_rect)
            
            # Map name
            if map_name:
                map_text = self.font_small.render(f"Map: {map_name}", True, CYAN)
                map_rect = map_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
                screen.blit(map_text, map_rect)
            
            # Show wave/enemies defeated for endless mode
            if game_mode == "Endless Mode":
                wave_text = self.font_small.render(f"Enemies Defeated: {enemies_defeated} | Wave: {enemies_defeated + 1}", True, GREEN)
                wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
                screen.blit(wave_text, wave_rect)
        
        # Controls
        controls = self.font_small.render("A/D: Move | W: Jump | SPACE: Attack | ESC: Menu", True, GRAY)
        controls_rect = controls.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(controls, controls_rect)
    
    def draw_health_bar(self, screen, x, y, width, height, current, maximum, label):
        """Draw a health bar"""
        # Background
        pygame.draw.rect(screen, RED, (x, y, width, height))
        
        # Health
        health_width = (current / maximum) * width
        pygame.draw.rect(screen, GREEN, (x, y, health_width, height))
        
        # Border
        pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)
        
        # Text
        health_text = self.font_small.render(f"{label}: {int(current)}/{int(maximum)}", True, WHITE)
        screen.blit(health_text, (x + 10, y + 5))
    
    def draw_game_over(self, screen, winner, game_mode=None, difficulty=None, enemies_defeated=0):
        """Draw game over screen"""
        screen.fill(BG_COLOR)
        
        # Game Over title
        game_over = self.font_large.render("GAME OVER", True, RED)
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(game_over, game_over_rect)
        
        # Winner
        winner_text = self.font_medium.render(f"{winner} Wins!", True, YELLOW)
        winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(winner_text, winner_rect)
        
        # Game details
        if game_mode:
            details = self.font_small.render(f"Mode: {game_mode} | Difficulty: {difficulty.upper()}", True, WHITE)
            details_rect = details.get_rect(center=(SCREEN_WIDTH // 2, 280))
            screen.blit(details, details_rect)
            
            # Show score for endless mode
            if game_mode == "Endless Mode":
                score = self.font_medium.render(f"Enemies Defeated: {enemies_defeated}", True, GREEN)
                score_rect = score.get_rect(center=(SCREEN_WIDTH // 2, 340))
                screen.blit(score, score_rect)
        
        # Return to menu options
        option1 = self.font_medium.render("Press ENTER to return to menu", True, WHITE)
        option1_rect = option1.get_rect(center=(SCREEN_WIDTH // 2, 450))
        screen.blit(option1, option1_rect)
        
        option2 = self.font_medium.render("Press SPACE to play again", True, GREEN)
        option2_rect = option2.get_rect(center=(SCREEN_WIDTH // 2, 520))
        screen.blit(option2, option2_rect)
    
    def draw_options(self, screen):
        """Draw options menu"""
        screen.fill(BG_COLOR)
        
        # Title
        title = self.font_large.render("Options", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)
        
        # Placeholder
        placeholder = self.font_medium.render("Options Menu (Placeholder)", True, WHITE)
        placeholder_rect = placeholder.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(placeholder, placeholder_rect)
        
        # Back instruction
        back = self.font_medium.render("Press '1' to return to menu", True, GRAY)
        back_rect = back.get_rect(center=(SCREEN_WIDTH // 2, 500))
        screen.blit(back, back_rect)

