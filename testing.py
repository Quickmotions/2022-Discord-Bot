import os
import random
from datetime import datetime
import time

from rpg.player import load_player, save_player, Player, check_for_missing, Job, Deck
from rpg.items import ItemManager, save_items, load_items, Card, Material, Equipment
from rpg.combat import Combat
# testing
if __name__ == '__main__':
    # player loading saving test
    player = load_player(482271768451612683, "Fungus")
    save_player(player)

    # player check for missing test
    class Skills:
        def __init__(self):
            # combat
            stats = ["health", "strength", "block", "magic", "agility",
                     "woodcutting", "fishing"]

            self.level = {}
            self.xp = {}
            self.xp_needed = {}

            for stat in stats:
                self.level[stat] = 0
                self.xp[stat] = 0
                self.xp_needed[stat] = 100


    class Player:
        def __init__(self):
            self.user_id = 1222
            self.skills = Skills()


    empty_player = Player()
    # check_for_missing(empty_player)

    # time difference test
    start = datetime.now()
    time.sleep(0)
    now = datetime.now()

    time_difference = now - start

    # job test
    player = load_player(482271768451612683, "Fungus")

    player.job = Job()
    save_player(player)

    # items test
    items = load_items()
    items.add(Card(id="slash", name="Slash", description="Deal 6 (strength) Damage",
                   card_type="attack", rarity="common", damage=6, skill_type="strength"))
    items.add(Card(id="defend", name="Defend", description="Block 5 (block) Damage",
                   card_type="attack", rarity="common", block=5, skill_type="block"))
    items.add(Card(id="bash", name="Bash", description="Deal 14 (strength) Damage, Costs 2 energy", cost=2,
                   card_type="attack", rarity="common", damage=14, skill_type="strength"))
    items.add(Card(id="bandage", name="Bandage", description="Heal 8 (healing) Damage",
                   card_type="attack", rarity="common", healing=8, skill_type="healing"))
    items.add(Material(id="lootbox", name="Daily Lootbox", description="Open for goodies"))
    save_items(items)
