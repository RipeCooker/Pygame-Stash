"""Adventure101 - refactored into a Game class for clarity and reuse.

This preserves the original story and choices while organizing code
into small methods that can be reused or tested.
"""

from typing import Optional
import sys


class Game:
    def __init__(self) -> None:
        self.name: Optional[str] = None
        self.lives: int = 3
        self.inventory = []

    def prompt(self, text: str) -> str:
        return input(text)

    def pause(self, text: str = "Press Enter to continue...") -> None:
        input(text)

    def lose_life(self, amount: int = 1) -> None:
        self.lives -= amount
        print(f"You lose {amount} life{'s' if amount>1 else ''}.")
        if self.lives <= 0:
            print("You have no lives left. Game Over.")
            sys.exit()
        print(f"You have {self.lives} lives left.")

    def choose(self, prompt_text: str, valid: Optional[list[str]] = None) -> str:
        choice = input(prompt_text).strip()
        if valid:
            return choice if choice in valid else ""
        return choice

    def start(self) -> None:
        self.name = self.prompt("Enter your name: ")
        print(f"Welcome to Adventure101, {self.name}!")
        print("In this adventure, you will make choices that affect your journey.")
        print("You start with 3 lives. Make wise choices to survive and complete your adventure.")
        print("Remember, some choices may lead to losing a life.")
        print("Most importantly, have fun!")
        print(f"Let the adventure begin, {self.name}!")
        self.pause("Press Enter to start your adventure...")
        self.setting_the_scene()

    def setting_the_scene(self) -> None:
        print("You are a normal kid living a boring life.")
        print("One day, you lash out and run away from home.")
        print("You walk for hours until you turn back and run straight to your home.")
        print("Instead of your home, you see darkness and faint.")
        self.pause()
        print("You wake up with no memories.")
        choice1 = self.choose("Do you want to explore your surroundings? (yes/no) ").lower()
        if choice1 == "yes":
            self.village_outskirts()
        else:
            print("You decide not to explore and continue wandering.")
        self.pause("Press Enter to turn to the dark alley...")
        self.underground_alley()

    def village_outskirts(self) -> None:
        print("You walk around and find a village.")
        print("You see a shop, a tavern, and a blacksmith.")
        self.pause()
        print("Where do you want to go?")
        print("1. Shop")
        print("2. Tavern")
        print("3. Blacksmith")
        choice2 = self.choose("Enter the number of your choice: ", ["1", "2", "3"]) or ""
        if choice2 == "1":
            print("You enter the shop and buy a health potion.")
            self.inventory.append("health potion")
        elif choice2 == "2":
            print("You enter the tavern and learn about a nearby dungeon filled with treasures.")
        elif choice2 == "3":
            print("You enter the blacksmith and buy a basic sword.")
            self.inventory.append("basic sword")
        else:
            print("Invalid choice. You leave the village and find a bush of berries!")
            choice3 = self.choose("Do you want to eat them? (yes/no) ").lower()
            if choice3 == "yes":
                print("You eat the berries and gain some health.")
            else:
                print("You avoid the berries, but later collapse from weakness.")
                self.lose_life()

    def underground_alley(self) -> None:
        print("You fall through a hidden trapdoor and land in a dark alley.")
        print(f"You have {self.lives} lives left.")
        self.pause()
        print("You find a cloaked figure who offers to help.")
        print("1. Accept the figure's help.")
        print("2. Decline and explore the alley on your own.")
        choice4 = self.choose("Enter the number of your choice: ", ["1", "2"]) or ""
        if choice4 == "1":
            print("The figure guides you to a safe exit from the alley.")
        else:
            print("You explore the alley and encounter hostile creatures.")
            print("You try to fight but get overwhelmed.")
            self.lose_life()
            print("You manage to escape and find a mysterious potion on the ground.")
            choice5 = self.choose("Do you want to drink it? (yes/no) ").lower()
            if choice5 == "yes":
                print("You drink the potion and feel a surge of energy.")
            else:
                print("You decide not to drink it, but later collapse from unknown pain.")
                self.lose_life()
        print("You continue your adventure...")
        self.dragon_encounter()

    def dragon_encounter(self) -> None:
        print("You find a dragon blocking your path!")
        print("1. Fight the dragon.")
        print("2. Try to sneak around the dragon.")
        choice6 = self.choose("Enter the number of your choice: ", ["1", "2"]) or ""
        if choice6 == "1":
            print("You bravely fight the dragon but get badly injured.")
            self.lose_life()
            print("You manage to escape the dragon and continue your adventure.")
        else:
            print("You successfully sneak around the dragon and continue your adventure.")
        print(f"Congratulations! You have completed this part of your adventure with {self.lives} lives left.")
        print("You suddenly feel guilt about leaving your family behind and decide to return home.")
        self.pause()
        self.return_home()

    def return_home(self) -> None:
        print("You walk back to the village and meet a warrior who offers a trade.")
        print("1. Trade your sword for a shield.")
        print("2. Keep your sword and continue home.")
        print("3. Attack the warrior to take both items.")
        choice7 = self.choose("Enter the number of your choice: ", ["1", "2", "3"]) or ""
        if choice7 == "1":
            if "basic sword" in self.inventory:
                self.inventory.remove("basic sword")
            self.inventory.append("shield")
            print("You trade your sword for a shield. The warrior wishes you luck.")
        elif choice7 == "2":
            print("You keep your sword and continue home. The warrior nods in approval.")
        elif choice7 == "3":
            print("You attack but are overpowered by the warrior.")
            self.lose_life()
            print("The warrior lets you go with a warning.")
        print("You continue your journey home.")
        print("You enter your home, but find it empty.")
        print("What will you do?")
        print("1: Search the house for clues.")
        print("2: Investigate other areas in the village.")
        print("3: Sit and wait for someone to return.")
        choice8 = self.choose("Enter the number of your choice: ", ["1", "2", "3"]) or ""
        if choice8 == "1":
            print("You search the house and find a hidden letter with a threat.")
            print("You decide to prepare for their return.")
        elif choice8 == "2":
            print("You investigate the village and find signs of a struggle. You gather allies.")
        else:
            print("You sit and wait, but no one returns. You lose a life due to hunger.")
            self.lose_life()
        self.chambers()

    def chambers(self) -> None:
        print("You explore the basement and find a hidden chamber with ancient artifacts.")
        print(f"You have {self.lives} lives left.")
        self.pause()
        print("In the chamber you find a familiar face — your long lost sibling!")
        print("They say they left the threats and reveal a complicated past.")
        print("Will you:")
        print("1: Forgive your sibling and welcome them back.")
        print("2: Reject them and ask them to leave.")
        print("3: Ask why they did it.")
        choice9 = self.choose("Enter the number of your choice: ", ["1", "2", "3"]) or ""
        if choice9 == "1":
            print("They betray you and throw you into a pit.")
            self.lose_life()
            print("You manage to climb out and continue.")
        elif choice9 == "2":
            print("They curse you and disappear. You feel brokenhearted.")
            self.lose_life()
        else:
            print("You ask why. They challenge you to a duel.")
            print("1: Accept the duel.")
            print("2: Try to negotiate peace.")
            print("3: Run away.")
            choice10 = self.choose("Enter the number of your choice: ", ["1", "2", "3"]) or ""
            if choice10 == "3":
                print("You run away, losing a life while escaping.")
                self.lose_life()
            else:
                print("You fight and later meet the warrior who provides armor and a shield.")
                print("Will you accept their help?")
                print("1: Accept the warrior's help.")
                print("2: Refuse and face your sibling alone.")
                choice11 = self.choose("Enter the number of your choice: ", ["1", "2"]) or ""
                if choice11 == "1":
                    print("You accept the warrior's help and prepare for battle.")
                else:
                    print("You refuse, lose the battle, and lose a life.")
                    self.lose_life()
                    print("With the warrior's help you eventually defeat your sibling.")
        print(f"Congratulations! You have completed your adventure with {self.lives} lives left.")
        print("You have reunited with your family and restored peace to the village.")
        self.pause("Press Enter to end the game...")
        print("Thank you for playing Adventure101!")


def main() -> None:
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
    print("They tell you they can't fight, but can give you a sheild and armor")

    print("Will you:")

