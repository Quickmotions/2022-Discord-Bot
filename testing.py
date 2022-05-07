import os
from datetime import datetime
import time

from rpg.player import load_player, save_player, Player, check_for_missing, Job
from rpg.items import ItemManager, save_items, load_items, Card, Material, Equipment

# testing
if __name__ == '__main__':
    # player loading saving test
    player = load_player(482271768451612683)
    player.inventory.items["test item"] = 12
    player.inventory.items["fake item"] = 297776
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
    check_for_missing(empty_player)

    # time difference test
    start = datetime.now()
    time.sleep(0)
    now = datetime.now()

    time_difference = now - start

    print(time_difference.total_seconds())

    # job test
    player = load_player(482271768451612683)

    player.job = Job()
    save_player(player)

    # items test
    items = load_items()
    print(items.item_list)
    # TODO: create in build item creator using slash commands.
    # TODO: automatic data backups
