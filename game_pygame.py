import pygame
import random
import sys
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
FONT_LARGE = pygame.font.Font(None, 36)
FONT_MEDIUM = pygame.font.Font(None, 24)
FONT_SMALL = pygame.font.Font(None, 18)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
YELLOW = (255, 200, 0)
BLUE = (50, 100, 200)
ORANGE = (255, 165, 0)

class GameState(Enum):
    INTRO = 1
    EXPLORING = 2
    EVENT = 3
    MENU = 4
    INVENTORY = 5
    HIRING = 6
    EATING = 7
    GAME_OVER = 8

class NPC:
    def __init__(self, npc_type):
        self.type = npc_type
        self.names = {
            "hermit": ["Marcus", "Jacob", "Solomon", "Thomas"],
            "villager": ["Emma", "James", "Sarah", "David", "Alice"],
            "merchant": ["Zeke", "Petra", "Silas", "Iris"]
        }
        self.name = random.choice(self.names.get(npc_type, ["Stranger"]))
        self.personality = random.choice(["kind", "gruff", "mysterious", "cheerful"])
        
    def greet(self):
        greetings = {
            "kind": f"{self.name} smiles warmly at you.",
            "gruff": f"{self.name} grunts in acknowledgment.",
            "mysterious": f"{self.name} studies you with an unreadable expression.",
            "cheerful": f"{self.name} greets you enthusiastically!"
        }
        return greetings.get(self.personality, f"{self.name} nods at you.")

class HiredNPC:
    def __init__(self, npc_type, name):
        self.type = npc_type
        self.name = name
        self.effectiveness = random.randint(60, 100)
        self.loyalty = 50
        self.cost_per_day = {"hunter": 10, "gatherer": 5, "scout": 8, "cook": 7}.get(npc_type, 5)
        self.morale = 100

class Quest:
    def __init__(self, quest_id, title, description, reward_items):
        self.id = quest_id
        self.title = title
        self.description = description
        self.reward_items = reward_items
        self.completed = False

class SurvivalGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Survival: Lost in the Wild - Pygame Edition")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.INTRO
        
        # Player stats
        self.player_name = ""
        self.health = 100
        self.hunger = 50
        self.inventory = []
        self.location = "forest"
        self.day = 1
        self.won = False
        self.game_over = False
        self.ending_type = None
        
        # Game data
        self.events_triggered = set()
        self.reputation = {"villagers": 0, "hermit": 0}
        self.crafted_items = set()
        self.visited_locations = set()
        self.npcs = {}
        self.hired_npcs = []
        self.poison_counter = 0
        self.available_gold = 0
        self.easter_eggs_found = set()
        
        # UI state
        self.current_event = None
        self.current_choices = []
        self.message_log = []
        self.input_text = ""
        self.input_active = False
        
        self.locations = ["forest", "mountain", "village", "river", "cabin", "ruins", "hermit_cave"]
        
    def add_message(self, message):
        self.message_log.append(message)
        if len(self.message_log) > 10:
            self.message_log.pop(0)
    
    def draw_intro(self):
        self.screen.fill(DARK_GRAY)
        
        title = FONT_LARGE.render("SURVIVAL: Lost in the Wild", True, YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        subtitle = FONT_MEDIUM.render("A Pygame Adventure", True, LIGHT_GRAY)
        self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 150))
        
        prompt = FONT_SMALL.render("Enter your name and press ENTER:", True, WHITE)
        self.screen.blit(prompt, (50, 300))
        
        # Draw input box
        input_rect = pygame.Rect(50, 350, 300, 40)
        pygame.draw.rect(self.screen, WHITE, input_rect, 2)
        text_surf = FONT_MEDIUM.render(self.input_text, True, WHITE)
        self.screen.blit(text_surf, (60, 360))
        
        story = [
            "You wake up in a dense forest with no memory of how you got there.",
            "Your goal: survive for 7 days and escape the wilderness.",
            "",
            "Manage your health and hunger carefully.",
            "Hire NPCs to help with hunting and cooking.",
            "Watch out for poison from eating raw meat!"
        ]
        
        y = 450
        for line in story:
            text = FONT_SMALL.render(line, True, LIGHT_GRAY)
            self.screen.blit(text, (50, y))
            y += 30
    
    def draw_main_screen(self):
        self.screen.fill(DARK_GRAY)
        
        # Header
        header = FONT_LARGE.render(f"DAY {self.day} - {self.player_name}", True, YELLOW)
        self.screen.blit(header, (20, 20))
        
        # Stats bar
        stats_text = f"Health: {self.health}/100 | Hunger: {self.hunger}/100 | Gold: {self.available_gold}"
        stats_surf = FONT_MEDIUM.render(stats_text, True, GREEN)
        self.screen.blit(stats_surf, (20, 70))
        
        if self.poison_counter > 0:
            poison_text = f"⚠ Poison: {self.poison_counter}%"
            poison_surf = FONT_MEDIUM.render(poison_text, True, RED)
            self.screen.blit(poison_surf, (20, 100))
        
        if len(self.hired_npcs) > 0:
            hired_text = f"Hired NPCs: {len(self.hired_npcs)}"
            hired_surf = FONT_MEDIUM.render(hired_text, True, BLUE)
            self.screen.blit(hired_surf, (SCREEN_WIDTH - 300, 70))
        
        # Location
        loc_text = f"Location: {self.location.title()}"
        loc_surf = FONT_MEDIUM.render(loc_text, True, WHITE)
        self.screen.blit(loc_surf, (20, 150))
        
        # Inventory
        inv_title = FONT_MEDIUM.render("Inventory:", True, LIGHT_GRAY)
        self.screen.blit(inv_title, (20, 200))
        
        if self.inventory:
            inv_text = ", ".join(self.inventory[:5])
            if len(self.inventory) > 5:
                inv_text += f", +{len(self.inventory) - 5} more"
            inv_surf = FONT_SMALL.render(inv_text, True, WHITE)
            self.screen.blit(inv_surf, (20, 230))
        else:
            empty_surf = FONT_SMALL.render("Empty", True, LIGHT_GRAY)
            self.screen.blit(empty_surf, (20, 230))
        
        # Message log
        msg_title = FONT_MEDIUM.render("Events:", True, LIGHT_GRAY)
        self.screen.blit(msg_title, (20, 300))
        
        y = 330
        for msg in self.message_log[-6:]:
            msg_surf = FONT_SMALL.render(msg[:80], True, WHITE)
            self.screen.blit(msg_surf, (20, y))
            y += 25
        
        # Menu options
        menu_title = FONT_MEDIUM.render("What do you do?", True, YELLOW)
        self.screen.blit(menu_title, (600, 200))
        
        options = [
            "[1] Explore",
            "[2] Rest",
            "[3] Forage",
            "[4] Inventory",
            "[5] Craft",
            "[6] Travel",
            "[7] Hire NPCs",
            "[8] Eat/Cook",
            "[Q] Quit"
        ]
        
        y = 240
        for opt in options:
            opt_surf = FONT_SMALL.render(opt, True, LIGHT_GRAY)
            self.screen.blit(opt_surf, (600, y))
            y += 30
    
    def draw_event_screen(self):
        self.screen.fill(DARK_GRAY)
        
        # Header
        header = FONT_LARGE.render("Event", True, YELLOW)
        self.screen.blit(header, (SCREEN_WIDTH//2 - header.get_width()//2, 50))
        
        # Event description
        if self.current_event:
            event_surf = FONT_MEDIUM.render(self.current_event, True, WHITE)
            self.screen.blit(event_surf, (100, 150))
        
        # Message log
        y = 250
        for msg in self.message_log[-4:]:
            msg_surf = FONT_SMALL.render(msg[:100], True, LIGHT_GRAY)
            self.screen.blit(msg_surf, (100, y))
            y += 30
        
        # Choices
        choice_title = FONT_MEDIUM.render("Choose:", True, YELLOW)
        self.screen.blit(choice_title, (100, 400))
        
        y = 440
        for i, choice in enumerate(self.current_choices, 1):
            choice_text = f"[{i}] {choice}"
            choice_surf = FONT_SMALL.render(choice_text, True, LIGHT_GRAY)
            self.screen.blit(choice_surf, (120, y))
            y += 35
    
    def draw_inventory_screen(self):
        self.screen.fill(DARK_GRAY)
        
        title = FONT_LARGE.render("Inventory", True, YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        if not self.inventory:
            empty_surf = FONT_MEDIUM.render("Your inventory is empty", True, LIGHT_GRAY)
            self.screen.blit(empty_surf, (SCREEN_WIDTH//2 - empty_surf.get_width()//2, 200))
        else:
            y = 150
            for i, item in enumerate(self.inventory, 1):
                item_text = f"{i}. {item}"
                item_surf = FONT_SMALL.render(item_text, True, WHITE)
                self.screen.blit(item_surf, (100, y))
                y += 30
        
        back_text = FONT_SMALL.render("Press SPACE to go back", True, LIGHT_GRAY)
        self.screen.blit(back_text, (SCREEN_WIDTH//2 - back_text.get_width()//2, SCREEN_HEIGHT - 50))
    
    def draw_hiring_screen(self):
        self.screen.fill(DARK_GRAY)
        
        title = FONT_LARGE.render("Hire NPCs", True, YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        gold_text = FONT_MEDIUM.render(f"Gold: {self.available_gold}", True, YELLOW)
        self.screen.blit(gold_text, (50, 120))
        
        if self.hired_npcs:
            hired_title = FONT_MEDIUM.render("Your Team:", True, LIGHT_GRAY)
            self.screen.blit(hired_title, (50, 170))
            
            y = 210
            for npc in self.hired_npcs:
                npc_text = f"{npc.name} ({npc.type}) - Eff: {npc.effectiveness}% | Cost: {npc.cost_per_day}/day"
                npc_surf = FONT_SMALL.render(npc_text, True, WHITE)
                self.screen.blit(npc_surf, (70, y))
                y += 30
        
        available_title = FONT_MEDIUM.render("Available for Hire:", True, LIGHT_GRAY)
        self.screen.blit(available_title, (50, 400))
        
        options = [
            "[1] Hunter (10 gold/day)",
            "[2] Gatherer (5 gold/day)",
            "[3] Scout (8 gold/day)",
            "[4] Cook (7 gold/day)",
            "[5] Back"
        ]
        
        y = 440
        for opt in options:
            opt_surf = FONT_SMALL.render(opt, True, LIGHT_GRAY)
            self.screen.blit(opt_surf, (70, y))
            y += 35
    
    def draw_game_over_screen(self):
        self.screen.fill(DARK_GRAY)
        
        if self.won:
            title = FONT_LARGE.render("VICTORY!", True, GREEN)
        else:
            title = FONT_LARGE.render("GAME OVER", True, RED)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        stats = [
            f"Days Survived: {self.day}",
            f"Final Health: {self.health}",
            f"Final Hunger: {self.hunger}",
            f"Items Collected: {len(self.inventory)}",
            f"Items Crafted: {len(self.crafted_items)}",
            f"Gold Found: {self.available_gold}",
            f"Reputation (Villagers): {self.reputation['villagers']}",
            f"Reputation (Hermit): {self.reputation['hermit']}",
            f"Secrets Found: {len(self.easter_eggs_found)}"
        ]
        
        y = 250
        for stat in stats:
            stat_surf = FONT_SMALL.render(stat, True, WHITE)
            self.screen.blit(stat_surf, (SCREEN_WIDTH//2 - stat_surf.get_width()//2, y))
            y += 35
        
        restart = FONT_MEDIUM.render("Press SPACE to return to menu", True, LIGHT_GRAY)
        self.screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, SCREEN_HEIGHT - 50))
    
    def explore(self):
        event_roll = random.randint(1, 100)
        
        if self.location == "forest":
            if event_roll < 50:
                self.current_event = "You find berry bushes!"
                self.current_choices = ["Gather berries", "Keep moving"]
                self.add_message("Berry bushes found in the forest.")
            else:
                self.current_event = "A wolf appears!"
                self.current_choices = ["Run away", "Stand ground", "Offer food"]
                self.add_message("A wolf emerges from the trees!")
                
        elif self.location == "village":
            self.current_event = f"You meet {self.npcs['villager_1'].name} from the village"
            self.current_choices = ["Talk to them", "Stay hidden"]
            self.add_message(f"You see {self.npcs['villager_1'].name} approaching.")
            
        elif self.location == "river":
            self.current_event = "You reach a crystal-clear river"
            self.current_choices = ["Try to fish", "Collect water"]
            self.add_message("You find a river with fish!")
            
        elif self.location == "mountain":
            if event_roll < 50:
                self.current_event = "You discover a cave entrance"
                self.current_choices = ["Enter the cave", "Pass by"]
                self.add_message("A cave entrance appears!")
            else:
                self.current_event = "A storm is approaching!"
                self.current_choices = ["Take shelter", "Keep moving"]
                self.add_message("Dark clouds roll in...")
                
        elif self.location == "cabin":
            self.current_event = "You find an abandoned cabin"
            self.current_choices = ["Enter cautiously", "Walk away"]
            self.add_message("An old cabin appears in the distance.")
            
        elif self.location == "ruins":
            self.current_event = "Ancient ruins overgrown with vines"
            self.current_choices = ["Explore", "Leave"]
            self.add_message("You discover ancient ruins!")
            
        elif self.location == "hermit_cave":
            self.current_event = f"You meet the hermit {self.npcs['hermit'].name}"
            self.current_choices = ["Greet", "Ask for help", "Leave"]
            self.add_message(f"The hermit {self.npcs['hermit'].name} greets you.")
        
        self.state = GameState.EVENT
    
    def rest(self):
        self.health = min(100, self.health + 10)
        self.hunger = min(100, self.hunger + 5)
        self.add_message("You rest and recover.")
        self.next_day()
        self.state = GameState.EXPLORING
    
    def forage(self):
        if random.randint(1, 100) > 60:
            self.inventory.append("foraged_berries")
            self.add_message("Found some edible berries!")
        else:
            self.add_message("Found nothing valuable.")
        self.next_day()
        self.state = GameState.EXPLORING
    
    def apply_poison_damage(self):
        if self.poison_counter > 0:
            damage = int(self.poison_counter * 0.5)
            self.health = max(0, self.health - damage)
            self.poison_counter = max(0, self.poison_counter - 10)
            if damage > 0:
                self.add_message(f"⚠ Poison damage: {damage} health lost!")
    
    def hire_npc(self, npc_type):
        available_names = {
            "hunter": ["Garrett", "Helena", "Quinn", "Roan"],
            "gatherer": ["Felix", "Iris", "Milo", "Nina"],
            "scout": ["Axel", "Sage", "Kai", "Scout"],
            "cook": ["Bruno", "Rosa", "Claude", "Mira"]
        }
        cost = {"hunter": 10, "gatherer": 5, "scout": 8, "cook": 7}[npc_type]
        
        if self.available_gold >= cost:
            hired_npc = HiredNPC(npc_type, random.choice(available_names.get(npc_type, ["Worker"])))
            self.hired_npcs.append(hired_npc)
            self.available_gold -= cost
            self.add_message(f"Hired {hired_npc.name} the {npc_type}!")
        else:
            self.add_message(f"Not enough gold! Need {cost}, have {self.available_gold}")
    
    def eat_food(self, food_item):
        if food_item == "raw_meat":
            cooks = [npc for npc in self.hired_npcs if npc.type == "cook"]
            if cooks:
                self.inventory.remove(food_item)
                self.inventory.append("cooked_meat")
                self.health = min(100, self.health + 5)
                self.hunger = max(0, self.hunger - 25)
                self.add_message(f"{cooks[0].name} cooked the meat for you!")
            else:
                self.inventory.remove(food_item)
                self.health = max(0, self.health - 5)
                self.hunger = max(0, self.hunger - 20)
                poison_increase = random.randint(15, 35)
                self.poison_counter += poison_increase
                self.add_message(f"⚠ Ate raw meat! Poison +{poison_increase}%")
        elif food_item in ["cooked_meat", "venison"]:
            self.inventory.remove(food_item)
            self.health = min(100, self.health + 10)
            self.hunger = max(0, self.hunger - 25)
            self.add_message(f"Delicious {food_item}! Restored health.")
        elif "fish" in food_item:
            self.inventory.remove(food_item)
            self.health = min(100, self.health + 8)
            self.hunger = max(0, self.hunger - 20)
            self.add_message("Fresh fish restored health!")
        else:
            self.inventory.remove(food_item)
            self.health = min(100, self.health + 5)
            self.hunger = max(0, self.hunger - 15)
            self.add_message(f"Ate {food_item}.")
    
    def next_day(self):
        self.day += 1
        self.hunger = min(100, self.hunger + random.randint(5, 15))
        if "warm_bed" not in self.inventory:
            self.health = max(0, self.health - random.randint(1, 5))
        self.apply_poison_damage()
        self.check_end_conditions()
    
    def check_end_conditions(self):
        if self.health <= 0:
            self.game_over = True
            self.won = False
            self.add_message(f"{self.player_name} collapsed from exhaustion.")
            self.state = GameState.GAME_OVER
        elif self.hunger >= 90:
            self.game_over = True
            self.won = False
            self.add_message(f"{self.player_name} starved.")
            self.state = GameState.GAME_OVER
        elif self.day >= 7 and self.location == "village":
            self.game_over = True
            self.won = True
            self.add_message("Helicopter arrived! You escaped!")
            self.state = GameState.GAME_OVER
        elif self.day >= 8:
            self.game_over = True
            self.won = False
            self.add_message("You ran out of time. Helicopter is gone.")
            self.state = GameState.GAME_OVER
    
    def handle_input(self, event):
        if self.state == GameState.INTRO:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.input_text:
                        self.player_name = self.input_text
                        self.npcs["hermit"] = NPC("hermit")
                        self.npcs["villager_1"] = NPC("villager")
                        self.npcs["merchant"] = NPC("merchant")
                        self.state = GameState.EXPLORING
                        self.add_message(f"Welcome, {self.player_name}!")
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    if len(self.input_text) < 20:
                        self.input_text += event.unicode
        
        elif self.state == GameState.EXPLORING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.explore()
                elif event.key == pygame.K_2:
                    self.rest()
                elif event.key == pygame.K_3:
                    self.forage()
                elif event.key == pygame.K_4:
                    self.state = GameState.INVENTORY
                elif event.key == pygame.K_5:
                    self.add_message("Crafting not yet implemented in GUI")
                elif event.key == pygame.K_6:
                    self.add_message("Choose a location: [F]orest [V]illage [R]iver [M]ountain [C]abin [U]ins [H]ermit")
                    self.state = GameState.MENU
                elif event.key == pygame.K_7:
                    self.state = GameState.HIRING
                elif event.key == pygame.K_8:
                    if any("meat" in item or "fish" in item or "berries" in item or "food" in item for item in self.inventory):
                        self.state = GameState.EATING
                    else:
                        self.add_message("No food to eat!")
                elif event.key == pygame.K_q:
                    self.running = False
        
        elif self.state == GameState.INVENTORY:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = GameState.EXPLORING
        
        elif self.state == GameState.HIRING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.hire_npc("hunter")
                elif event.key == pygame.K_2:
                    self.hire_npc("gatherer")
                elif event.key == pygame.K_3:
                    self.hire_npc("scout")
                elif event.key == pygame.K_4:
                    self.hire_npc("cook")
                elif event.key == pygame.K_5 or event.key == pygame.K_SPACE:
                    self.state = GameState.EXPLORING
        
        elif self.state == GameState.EATING:
            if event.type == pygame.KEYDOWN:
                food_items = [item for item in self.inventory if "meat" in item or "fish" in item or "berries" in item or "food" in item]
                if event.key - pygame.K_1 < len(food_items) and event.key >= pygame.K_1:
                    self.eat_food(food_items[event.key - pygame.K_1])
                    self.next_day()
                    self.state = GameState.EXPLORING
                elif event.key == pygame.K_SPACE:
                    self.state = GameState.EXPLORING
        
        elif self.state == GameState.EVENT:
            if event.type == pygame.KEYDOWN:
                if event.key - pygame.K_1 < len(self.current_choices):
                    choice_idx = event.key - pygame.K_1
                    self.add_message(f"You chose: {self.current_choices[choice_idx]}")
                    self.next_day()
                    self.state = GameState.EXPLORING
        
        elif self.state == GameState.GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__init__()
        
        elif self.state == GameState.MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.location = "forest"
                    self.state = GameState.EXPLORING
                elif event.key == pygame.K_v:
                    self.location = "village"
                    self.state = GameState.EXPLORING
                elif event.key == pygame.K_r:
                    self.location = "river"
                    self.state = GameState.EXPLORING
                elif event.key == pygame.K_m:
                    self.location = "mountain"
                    self.state = GameState.EXPLORING
                elif event.key == pygame.K_c:
                    self.location = "cabin"
                    self.state = GameState.EXPLORING
                elif event.key == pygame.K_u:
                    self.location = "ruins"
                    self.state = GameState.EXPLORING
                elif event.key == pygame.K_h:
                    self.location = "hermit_cave"
                    self.state = GameState.EXPLORING
                elif event.key == pygame.K_SPACE:
                    self.state = GameState.EXPLORING
    
    def draw(self):
        if self.state == GameState.INTRO:
            self.draw_intro()
        elif self.state == GameState.EXPLORING:
            self.draw_main_screen()
        elif self.state == GameState.EVENT:
            self.draw_event_screen()
        elif self.state == GameState.INVENTORY:
            self.draw_inventory_screen()
        elif self.state == GameState.HIRING:
            self.draw_hiring_screen()
        elif self.state == GameState.EATING:
            self.draw_eating_screen()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over_screen()
        elif self.state == GameState.MENU:
            self.draw_travel_screen()
        
        pygame.display.flip()
    
    def draw_eating_screen(self):
        self.screen.fill(DARK_GRAY)
        
        title = FONT_LARGE.render("What do you want to eat?", True, YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        food_items = [item for item in self.inventory if "meat" in item or "fish" in item or "berries" in item or "food" in item]
        
        y = 150
        for i, item in enumerate(food_items, 1):
            food_text = f"[{i}] {item}"
            food_surf = FONT_SMALL.render(food_text, True, WHITE)
            self.screen.blit(food_surf, (100, y))
            y += 35
        
        back_text = FONT_SMALL.render("Press SPACE to go back", True, LIGHT_GRAY)
        self.screen.blit(back_text, (SCREEN_WIDTH//2 - back_text.get_width()//2, SCREEN_HEIGHT - 50))
    
    def draw_travel_screen(self):
        self.screen.fill(DARK_GRAY)
        
        title = FONT_LARGE.render("Where do you travel?", True, YELLOW)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        options = [
            "[F] Forest",
            "[V] Village",
            "[R] River",
            "[M] Mountain",
            "[C] Cabin",
            "[U] Ruins",
            "[H] Hermit Cave",
            "[SPACE] Cancel"
        ]
        
        y = 200
        for opt in options:
            opt_surf = FONT_SMALL.render(opt, True, LIGHT_GRAY)
            self.screen.blit(opt_surf, (SCREEN_WIDTH//2 - opt_surf.get_width()//2, y))
            y += 40
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SurvivalGame()
    game.run()
