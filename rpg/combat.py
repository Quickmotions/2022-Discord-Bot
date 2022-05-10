import disnake

from rpg.player import Player, PlayerCombat
from rpg.items import load_items


class Enemy:
    def __init__(self, name):
        pass


class Combat:
    def __init__(self, player: Player, enemy: Enemy):
        self.combat_player = PlayerCombat(player)
        self.player = player
        self.turn_num = 0
        self.turn = "player"
        self.combat_player.energy = self.combat_player.energy_max
        self.hand = self.combat_player.draw_hand()

    def next_turn(self):
        if self.turn == "player":
            self.turn = "enemy"
        else:
            self.turn = "player"

        # reset turn
        self.combat_player.energy = self.combat_player.energy_max
        self.combat_player.hand = self.combat_player.draw_hand()
        self.combat_player.block = 0

    def get_hand_list(self):
        items = load_items()
        hand_desc = ""
        num = 1
        for card in self.hand:
            card = items.item_list[card]
            hand_desc += f"**{num}** {card.name} - ||{card.description}||\n"
            num += 1

        return hand_desc
