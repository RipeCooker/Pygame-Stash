import pygame
import time

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lost in the Woods")

# Fonts and colors
font = pygame.font.SysFont("arial", 24)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Inventory
inventory = []

# Function to wrap text so it fits the screen width
def wrap_text(text, max_width):
    wrapped_lines = []
    for raw_line in text.split('\n'):
        words = raw_line.split(' ')
        current_line = ""
        for word in words:
            if not word and current_line == "":
                continue
            candidate = (current_line + " " + word).strip()
            if font.size(candidate)[0] <= max_width:
                current_line = candidate
            else:
                if current_line:
                    wrapped_lines.append(current_line)
                current_line = word
        if current_line:
            wrapped_lines.append(current_line)
        elif raw_line == "":
            wrapped_lines.append("")
    return wrapped_lines

# Function to render text
def draw_text(text):
    screen.fill(BLACK)
    lines = wrap_text(text, WIDTH - 40)
    for i, line in enumerate(lines):
        rendered = font.render(line, True, WHITE)
        screen.blit(rendered, (20, 20 + i * 30))
    pygame.display.flip()

# Function to show inventory
def show_inventory():
    draw_text("Inventory: " + ", ".join(inventory) if inventory else "Inventory is empty")
    time.sleep(2)

# Function to get input with inventory support
def get_input(prompt):
    user_text = ""
    draw_text(prompt)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                # Show inventory
                if event.key == pygame.K_i:
                    show_inventory()
                    draw_text(prompt + "\n" + user_text)
                # Submit input
                elif event.key == pygame.K_RETURN:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
        draw_text(prompt + "\n" + user_text)
    return user_text.lower()

# Function for non-interactive pauses with inventory access
def pause_text(text, seconds=2):
    start = time.time()
    while time.time() - start < seconds:
        draw_text(text)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                show_inventory()
                draw_text(text)

# Menu START
draw_text("Welcome to my game!Press any key to start.")
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            waiting = False
            pause_text("Get ready to start your adventure!", 2)
            pause_text("Press 'I' anytime to view your inventory.", 2)
            pause_text("Game is loading ...", 2)
            time.sleep(5)
            print("Assets Loaded. Starting game...")
# Menu END
pause_text("You find yourself lost in a dark forest.\nYou can barely see anything around you.", 3)
choice1 = get_input("Do you want to go left or right? (Type 'left' or 'right')")
if choice1 == "left":
    pause_text("You walk left and find a shiny object on the ground.", 3)
    choice2 = get_input("Do you want to pick it up? (yes/no)")
    if choice2 == "yes":
        inventory.append("shiny object")
        pause_text("You picked up the shiny object!", 2)
    else:
        pause_text("You leave the shiny object behind, and continue your journey.", 3)
    pause_text("Continuing your journey, you find a hut", 3)
    pause_text("You wonder why it is there in te middle of the forest.", 3)
    draw_text("You look closer and see no one is home.\nDo you want to enter the hut or keep walking? (Type 'enter' or 'walk away')")
    choice3 = get_input("Do you want to enter the hut or keep walking? (Type 'enter' or 'walk away')")
    if choice3 == "enter":
        pause_text("You find a map inside the hut!", 3)
        inventory.append("map")
        pause_text("You picked up the map!", 2)
        pause_text("You continue your journey")
    
    pause_text("You find a man sitting next to a camfire!", 3)
    pause_text("He holds an apple in his hand.", 3)
    choice5 = get_input("Do you take the apple or approach him? (Type 'take' or 'approach')")        
    if choice5 == "take":
                inventory.append("apple")
                pause_text("The old man catches you stealing his apple!", 3)
                pause_text("He says: Keep it. I don't need the apple anymore.", 3)
                pause_text("You ask:Why?", 3)
                pause_text("He says:Some things are better left unknown.", 3)
                pause_text("He stands up and tells you:Use that map to enter a small rock formation.", 3)
                pause_text("There is some sort of power that might help you.", 3)
                pause_text("You thank him and head towards the rock formation.", 3)
                pause_text("Do you want to head there or roam around some more?", 3)
                
                pause_text("You are blocked by a force field!", 3)
                if "shiny object" in inventory and "map" in inventory:
                        pause_text("You put the shiny object into the holder of the formation.", 3)
                        pause_text("Your shiny object,which is identified as a crystal,is not powerful enough")
                        if "shiny object" not in inventory:
                            pause_text("You don't have the required item to proceed.", 3)
                            pause_text("You search and find it nearby!", 3)
                            inventory.append("shiny object")
                            pause_text("You picked up the shiny object!", 2)
                        pause_text("You put the shiny object into the holder of the formation.", 3)
                        pause_text("The old man comes to you flying!", 3)
                        pause_text("He reveals to be a king, who became a ghost after a dark force destroyed his kingdom.", 3)
                        pause_text("He tells you to enter the formation.", 3)
                        pause_text("You suddenly get transported into a underground ruin!")
                        choice6 = get_input("do you want to put your hand into a glowing hole in the wall? (yes/no)")
                        if choice6 == "yes":
                            pause_text("You feel a surge of energy coursing through your body!", 3)
                            pause_text("You have gained magical powers!", 3)
                            pause_text("You can now clone objects you can identify!", 3)
                        if choice6 == "no":
                            pause_text("Nothing happens,so you put your hand away.", 3)
                            pause_text("A god tells you:Welcome to my trial!Use your ability to survive!", 3)
                            pause_text("Using your power,you complete the trial!", 3)
                            pause_text("You are teleported outside the rock formation!", 3)
                            pause_text("The ghost king appears again!", 3)
                            pause_text("He says:See that village over there? that is the survivor's haven.", 3)
                            pause_text("to be continued...", 3)