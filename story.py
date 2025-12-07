"""Story definitions for Story Mode.

Each entry in STORY is a node with a list of dialogues. A dialogue is a dict:
  {"speaker": str, "text": str, "map": optional map key}

If the final dialogue in a node includes a key "start_battle": True and an
"enemy" dict, the game will start a battle with the provided preset when the
dialogue finishes.
"""
from constants import *

STORY = [
    {
        "title": "Prologue",
        "dialogues": [
            {"speaker": "Narrator", "text": "Long ago, the kingdoms lived in peace..."},
            {"speaker": "Narrator", "text": "But darkness spread and challengers arose to test your strength."},
            {"speaker": "Mentor", "text": "You're ready. Travel to the Training Grounds and prove yourself." , "map": "training_ground"},
            {"speaker": "Mentor", "text": "Defeat the trainer to begin your journey.", "start_battle": True,
             "enemy": {"weapon": "stick", "color": RED, "health": 60, "speed": 3, "ai_update_freq": 40, "damage_multiplier": 0.8, "map": "training_ground"}}
        ]
    },
    {
        "title": "The Bandit Ambush",
        "dialogues": [
            {"speaker": "Villager", "text": "Thank you for rescuing our town! But bandits roam nearby...", "map": "village"},
            {"speaker": "Bandit Leader", "text": "You'll never leave with our treasure!", "start_battle": True,
             "enemy": {"weapon": "dagger", "color": DARK_RED, "health": 90, "speed": 5, "ai_update_freq": 25, "damage_multiplier": 1.0, "map": "village"}}
        ]
    },
    {
        "title": "Showdown",
        "dialogues": [
            {"speaker": "Mentor", "text": "You've come far. Face the champion in the Coliseum.", "map": "coliseum"},
            {"speaker": "Champion", "text": "I accept your challenge. Show me your strength!", "start_battle": True,
             "enemy": {"weapon": "sword", "color": GOLD, "health": 180, "speed": 6, "ai_update_freq": 18, "damage_multiplier": 1.2, "map": "coliseum"}}
        ]
    }
]
