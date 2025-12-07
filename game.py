"""Main game class"""
import pygame
import random
from constants import *
from story import STORY
from player import Player
from enemy import Enemy
from ui import UIManager
from map import Map

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ultimate Rumble")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"  # menu, mode_select, difficulty_select, map_select, weapon_select, color_select, playing, game_over
        self.ui = UIManager()
        
        # Game settings
        self.game_mode = None
        self.difficulty = "normal"
        self.difficulty_config = DIFFICULTY_LEVELS["normal"]
        self.current_level = 1
        self.enemies_defeated = 0
        
        # Player customization
        self.player_weapon = None
        self.player_color = None
        self.selected_weapon_index = 0
        self.selected_color_index = 0
        self.weapon_list = list(WEAPONS.keys())
        self.player_color_list = [BLUE, CYAN, PURPLE, LIME, MAGENTA, TEAL]
        
        # Map selection
        self.current_map = None
        self.map_list = list(MAPS.keys())
        self.selected_map_index = 0
        
        # Game objects
        self.player = None
        self.enemy = None
        self.all_sprites = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()

        # Story mode state
        self.story = STORY
        self.story_node_index = 0
        self.story_dialogue_index = 0
        self.in_story_battle = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == "menu":
                    if event.key == pygame.K_1:
                        self.state = "mode_select"
                    elif event.key == pygame.K_2:
                        self.show_options()
                    elif event.key == pygame.K_3:
                        self.running = False
                elif self.state == "mode_select":
                    if event.key == pygame.K_1:
                        self.game_mode = "Story Mode"
                        self.state = "difficulty_select"
                    elif event.key == pygame.K_2:
                        self.game_mode = "Endless Mode"
                        self.state = "difficulty_select"
                    elif event.key == pygame.K_3:
                        self.game_mode = "Rumble Mode"
                        self.state = "difficulty_select"
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                elif self.state == "difficulty_select":
                    if event.key == pygame.K_1:
                        self.difficulty = "easy"
                        self.difficulty_config = DIFFICULTY_LEVELS["easy"]
                        self.state = "map_select"
                    elif event.key == pygame.K_2:
                        self.difficulty = "normal"
                        self.difficulty_config = DIFFICULTY_LEVELS["normal"]
                        self.state = "map_select"
                    elif event.key == pygame.K_3:
                        self.difficulty = "hard"
                        self.difficulty_config = DIFFICULTY_LEVELS["hard"]
                        self.state = "map_select"
                    elif event.key == pygame.K_4:
                        self.difficulty = "insane"
                        self.difficulty_config = DIFFICULTY_LEVELS["insane"]
                        self.state = "map_select"
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "mode_select"
                elif self.state == "map_select":
                    if event.key == pygame.K_UP:
                        self.selected_map_index = (self.selected_map_index - 1) % len(self.map_list)
                    elif event.key == pygame.K_DOWN:
                        self.selected_map_index = (self.selected_map_index + 1) % len(self.map_list)
                    elif event.key == pygame.K_RETURN:
                        self.current_map = Map(self.map_list[self.selected_map_index])
                        self.state = "weapon_select"
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "difficulty_select"
                elif self.state == "weapon_select":
                    if event.key == pygame.K_UP:
                        self.selected_weapon_index = (self.selected_weapon_index - 1) % len(self.weapon_list)
                    elif event.key == pygame.K_DOWN:
                        self.selected_weapon_index = (self.selected_weapon_index + 1) % len(self.weapon_list)
                    elif event.key == pygame.K_RETURN:
                        self.player_weapon = self.weapon_list[self.selected_weapon_index]
                        self.state = "color_select"
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "difficulty_select"
                elif self.state == "color_select":
                    if event.key == pygame.K_UP:
                        self.selected_color_index = (self.selected_color_index - 1) % len(self.player_color_list)
                    elif event.key == pygame.K_DOWN:
                        self.selected_color_index = (self.selected_color_index + 1) % len(self.player_color_list)
                    elif event.key == pygame.K_RETURN:
                        self.player_color = self.player_color_list[self.selected_color_index]
                        # If Story Mode, start the story flow; otherwise start a single match
                        if self.game_mode == "Story Mode":
                            # prepare player and enter story state
                            player_health = self.difficulty_config["player_health"]
                            self.all_sprites.empty()
                            self.effects.empty()
                            self.player = Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, self.player_weapon, player_health, self.player_color)
                            self.all_sprites.add(self.player)
                            # initialize story indices
                            self.story_node_index = 0
                            self.story_dialogue_index = 0
                            self.in_story_battle = False
                            self.state = "story"
                            # set map from first dialogue if provided
                            first_node = self.story[self.story_node_index]
                            first_dialog = first_node.get("dialogues", [])[0]
                            if first_dialog and first_dialog.get("map"):
                                self.current_map = Map(first_dialog.get("map"))
                        else:
                            self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "weapon_select"
                elif self.state == "story":
                    # Advance dialog in story mode
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.advance_story()
                elif self.state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                    else:
                        self.player.handle_input(event)
                elif self.state == "game_over":
                    if event.key == pygame.K_RETURN:
                        self.state = "menu"
                    elif event.key == pygame.K_SPACE:
                        self.start_game()
                elif self.state == "options":
                    if event.key == pygame.K_1 or event.key == pygame.K_ESCAPE:
                        self.state = "menu"
        
        # Continuous key input for movement
        if self.state == "playing" and self.player:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.vel_x = -PLAYER_SPEED
                self.player.facing = -1
            elif keys[pygame.K_d]:
                self.player.vel_x = PLAYER_SPEED
                self.player.facing = 1
            else:
                self.player.vel_x = 0
            
            if keys[pygame.K_w] and self.player.on_ground:
                self.player.vel_y = -PLAYER_JUMP_POWER
                self.player.is_jumping = True
                self.player.on_ground = False
            
            if keys[pygame.K_SPACE]:
                self.player.is_attacking = True
    
    def start_game(self):
        # Clear old sprites
        self.all_sprites.empty()
        self.effects.empty()
        
        self.state = "playing"
        
        # Create player with selected weapon and color
        player_health = self.difficulty_config["player_health"]
        self.player = Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, self.player_weapon, player_health, self.player_color)
        
        # Get random weapon and color for enemy (randomized)
        enemy_weapon = random.choice(list(WEAPONS.keys()))
        enemy_color = random.choice([RED, ORANGE, DARK_RED, PINK, GOLD, YELLOW])
        
        # Create enemy with difficulty settings
        enemy_health = self.difficulty_config["enemy_health"]
        enemy_speed = self.difficulty_config["enemy_speed"]
        enemy_ai_freq = self.difficulty_config["enemy_ai_update_freq"]
        damage_mult = self.difficulty_config["enemy_damage_multiplier"]
        
        self.enemy = Enemy(SCREEN_WIDTH - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, enemy_weapon, 
                          enemy_health, enemy_speed, enemy_ai_freq, damage_mult, enemy_color)
        
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.enemy)

    def start_battle_with_preset(self, preset):
        """Create an enemy from a preset (used by story mode) and start the fight."""
        # Remove any existing enemy
        if self.enemy:
            try:
                self.enemy.kill()
            except Exception:
                pass

        weapon = preset.get("weapon", random.choice(list(WEAPONS.keys())))
        color = preset.get("color", random.choice([RED, ORANGE, DARK_RED, PINK, GOLD, YELLOW]))
        health = preset.get("health", self.difficulty_config["enemy_health"])
        speed = preset.get("speed", self.difficulty_config["enemy_speed"])
        ai_freq = preset.get("ai_update_freq", self.difficulty_config["enemy_ai_update_freq"])
        damage_mult = preset.get("damage_multiplier", self.difficulty_config["enemy_damage_multiplier"])

        # set map if provided
        if preset.get("map"):
            self.current_map = Map(preset.get("map"))

        self.enemy = Enemy(SCREEN_WIDTH - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, weapon, 
                          health, speed, ai_freq, damage_mult, color)
        self.all_sprites.add(self.enemy)
        self.in_story_battle = True
        self.state = "playing"

    def advance_story(self):
        """Advance the current story dialogue or trigger battles/next node."""
        if self.story_node_index >= len(self.story):
            # nothing left
            self.state = "game_over"
            self.ui.game_over_winner = "Player"
            return

        node = self.story[self.story_node_index]
        dialogues = node.get("dialogues", [])
        # if no dialogues, advance node
        if not dialogues:
            self.story_node_index += 1
            self.story_dialogue_index = 0
            return

        # if not at last dialogue, advance
        if self.story_dialogue_index < len(dialogues) - 1:
            self.story_dialogue_index += 1
            # update map if dialogue specifies
            dlg = dialogues[self.story_dialogue_index]
            if dlg.get("map"):
                self.current_map = Map(dlg.get("map"))
            return

        # last dialogue in node
        dlg = dialogues[self.story_dialogue_index]
        if dlg.get("start_battle"):
            preset = dlg.get("enemy", {})
            self.start_battle_with_preset(preset)
            return

        # no battle, move to next node
        self.story_node_index += 1
        self.story_dialogue_index = 0
        if self.story_node_index >= len(self.story):
            self.state = "game_over"
            self.ui.game_over_winner = "Player"
        else:
            # show next node's first dialogue and map
            next_node = self.story[self.story_node_index]
            first = next_node.get("dialogues", [])[0]
            if first and first.get("map"):
                self.current_map = Map(first.get("map"))
            self.state = "story"
    
    def show_options(self):
        self.state = "options"
    
    def spawn_new_enemy(self):
        """Spawn a new enemy for endless mode"""
        # Remove old enemy
        self.enemy.kill()
        
        # Get random weapon and color for new enemy
        enemy_weapon = random.choice(list(WEAPONS.keys()))
        enemy_color = random.choice([RED, ORANGE, DARK_RED, PINK, GOLD, YELLOW])
        
        # Increase difficulty slightly each round
        difficulty_multiplier = 1.0 + (self.enemies_defeated * 0.1)
        
        enemy_health = int(self.difficulty_config["enemy_health"] * difficulty_multiplier)
        enemy_speed = self.difficulty_config["enemy_speed"]
        enemy_ai_freq = max(10, int(self.difficulty_config["enemy_ai_update_freq"] * (1 - self.enemies_defeated * 0.05)))
        damage_mult = self.difficulty_config["enemy_damage_multiplier"] * difficulty_multiplier
        
        # Create new enemy with increased stats
        self.enemy = Enemy(SCREEN_WIDTH - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, enemy_weapon, 
                          enemy_health, enemy_speed, enemy_ai_freq, damage_mult, enemy_color)
        self.all_sprites.add(self.enemy)
    
    def update(self):
        if self.state == "playing":
            self.all_sprites.update()
            self.effects.update()
            
            # Check collisions
            self.check_collisions()
            
            # Reset attack flags after collision check
            if self.player:
                self.player.is_attacking = False
            if self.enemy:
                self.enemy.is_attacking = False
            
            # Check if player is dead
            if self.player.health <= 0:
                self.state = "game_over"
                self.ui.game_over_winner = "Enemy"
            # Check if enemy is dead
            elif self.enemy.health <= 0:
                # remove enemy sprite from groups
                try:
                    self.enemy.kill()
                except Exception:
                    pass

                if self.game_mode == "Endless Mode":
                    # Spawn new enemy in endless mode
                    self.spawn_new_enemy()
                    self.enemies_defeated += 1
                elif self.game_mode == "Story Mode" and self.in_story_battle:
                    # finished a story battle, advance the story
                    self.in_story_battle = False
                    self.enemies_defeated += 1
                    # advance to next story node
                    self.story_node_index += 1
                    self.story_dialogue_index = 0
                    if self.story_node_index >= len(self.story):
                        self.state = "game_over"
                        self.ui.game_over_winner = "Player"
                    else:
                        # set map for next node
                        next_node = self.story[self.story_node_index]
                        first = next_node.get("dialogues", [])[0]
                        if first and first.get("map"):
                            self.current_map = Map(first.get("map"))
                        self.state = "story"
                else:
                    # End game in other modes
                    self.state = "game_over"
                    self.ui.game_over_winner = "Player"
    
    def check_collisions(self):
        # Check attack collisions for player
        if self.player.is_attacking:
            distance = abs(self.player.rect.centerx - self.enemy.rect.centerx)
            if distance < 150 and self.player.attack_cooldown <= 0:  # Attack range
                damage = self.player.get_weapon_damage()
                self.enemy.take_damage(damage)
                self.player.attack_cooldown = 30  # Cooldown frames
                
                # Create hit effect
                effect_x = (self.player.rect.centerx + self.enemy.rect.centerx) // 2
                effect_y = (self.player.rect.centery + self.enemy.rect.centery) // 2
                self.create_hit_effect(effect_x, effect_y, damage)
        
        # Enemy AI attack
        if self.enemy.is_attacking:
            distance = abs(self.player.rect.centerx - self.enemy.rect.centerx)
            if distance < 150 and self.enemy.attack_cooldown <= 0:
                damage = self.enemy.get_weapon_damage()
                self.player.take_damage(damage)
                self.enemy.attack_cooldown = 30  # Cooldown frames
                
                # Create hit effect
                effect_x = (self.player.rect.centerx + self.enemy.rect.centerx) // 2
                effect_y = (self.player.rect.centery + self.enemy.rect.centery) // 2
                self.create_hit_effect(effect_x, effect_y, damage)
    
    def create_hit_effect(self, x, y, damage):
        """Create a visual effect for a hit"""
        from effects import DamageText
        effect = DamageText(x, y, damage)
        self.effects.add(effect)
    
    def draw(self):
        self.screen.fill(BG_COLOR)
        
        if self.state == "menu":
            self.ui.draw_menu(self.screen)
        elif self.state == "mode_select":
            self.ui.draw_mode_select(self.screen)
        elif self.state == "difficulty_select":
            self.ui.draw_difficulty_select(self.screen)
        elif self.state == "map_select":
            self.ui.draw_map_select(self.screen, self.map_list, self.selected_map_index)
        elif self.state == "weapon_select":
            self.ui.draw_weapon_select(self.screen, self.weapon_list, self.selected_weapon_index)
        elif self.state == "color_select":
            self.ui.draw_color_select(self.screen, self.player_color_list, self.selected_color_index)
        elif self.state == "playing":
            self.current_map.draw(self.screen)
            self.all_sprites.draw(self.screen)
            # Draw weapon overlays (use surfaces so they look like weapons)
            if self.player:
                info = self.player.get_weapon_draw_info()
                if info:
                    surf, rect, facing = info
                    draw_surf = surf
                    if facing == -1:
                        draw_surf = pygame.transform.flip(surf, True, False)
                    self.screen.blit(draw_surf, rect.topleft)
            if self.enemy:
                info = self.enemy.get_weapon_draw_info()
                if info:
                    surf, rect, facing = info
                    draw_surf = surf
                    if facing == -1:
                        draw_surf = pygame.transform.flip(surf, True, False)
                    self.screen.blit(draw_surf, rect.topleft)
            self.effects.draw(self.screen)
            self.ui.draw_game_ui(self.screen, self.player, self.enemy, self.game_mode, self.difficulty, self.current_level, self.enemies_defeated, self.current_map.display_name)
        elif self.state == "story":
            # Draw map and player, then show story dialog box
            if self.current_map:
                self.current_map.draw(self.screen)
            # draw player sprite
            if self.player:
                self.all_sprites.draw(self.screen)
            # draw UI small info
            self.ui.draw_game_ui(self.screen, self.player, self.enemy if self.enemy else Player(0,0,"stick"), self.game_mode, self.difficulty, self.current_level, self.enemies_defeated, self.current_map.display_name if self.current_map else None)

            # get current dialogue
            if self.story_node_index < len(self.story):
                node = self.story[self.story_node_index]
                dialogues = node.get("dialogues", [])
                if dialogues and self.story_dialogue_index < len(dialogues):
                    dlg = dialogues[self.story_dialogue_index]
                    speaker = dlg.get("speaker", "")
                    text = dlg.get("text", "")
                    title = node.get("title")
                    self.ui.draw_story(self.screen, speaker, text, title=title)
                else:
                    # nothing to show
                    pass
        elif self.state == "game_over":
            self.ui.draw_game_over(self.screen, self.ui.game_over_winner, self.game_mode, self.difficulty, self.enemies_defeated)
        elif self.state == "options":
            self.ui.draw_options(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
