"""
mood_engine.py
--------------
Resolves which mood the character should be in, picks a (mostly)
non-repeating message from data/messages.json, and maps moods to
their sprite-sheet asset paths.

Moods: idle | ringing | happy | sad | excited
"""
import json
import os
import random

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
MESSAGES_PATH = os.path.join(DATA_DIR, "messages.json")

SPRITE_PATHS = {
    "idle": os.path.join(ASSETS_DIR, "character_idle.png"),
    "ringing": os.path.join(ASSETS_DIR, "character_ringing.png"),
    "happy": os.path.join(ASSETS_DIR, "character_happy.png"),
    "sad": os.path.join(ASSETS_DIR, "character_sad.png"),
    "excited": os.path.join(ASSETS_DIR, "character_excited.png"),
}


def load_message_pools():
    with open(MESSAGES_PATH, "r") as f:
        return json.load(f)


class MoodEngine:
    """
    Keeps a small "recently used" buffer per mood so the same line
    doesn't repeat back-to-back, without needing any persistent state.
    """

    def __init__(self):
        self._pools = load_message_pools()
        self._recent = {mood: [] for mood in self._pools}

    def sprite_for(self, mood):
        return SPRITE_PATHS.get(mood, SPRITE_PATHS["idle"])

    def message_for(self, mood, commit_number=None):
        pool = self._pools.get(mood)
        if not pool:
            return ""
        recent = self._recent.setdefault(mood, [])
        choices = [m for m in pool if m not in recent] or pool
        choice = random.choice(choices)

        recent.append(choice)
        if len(recent) > max(1, len(pool) // 2):
            recent.pop(0)

        if commit_number is not None:
            choice = choice.replace("{n}", str(commit_number))
        return choice
