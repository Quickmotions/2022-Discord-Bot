import disnake

from rpg.player import Player, PlayerCombat
from rpg.items import load_items


class Enemy:
    def __init__(self, name: str = "Mob", hp: int = 1, damage: int = 1, block: int = 1, a_b_ratio: float = 0.5):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.block = block
        self.attack_block_ratio = a_b_ratio



class Combat:
    def __init__(self, player: Player, enemy: Enemy):
        self.combat_player = PlayerCombat(player)
        self.player = player
        self.turn_num = 0
        self.turn = "player"
        self.combat_player.energy = self.combat_player.energy_max
        self.hand = self.combat_player.draw_hand()
        self.used_cards = []

    def next_turn(self):
        if self.turn == "player":
            self.turn = "enemy"
        else:
            self.turn = "player"
        self.turn_num += 1

        # reset turn
        self.used_cards = []
        self.combat_player.energy = self.combat_player.energy_max
        self.combat_player.block = 0

        self.hand = self.combat_player.draw_hand()

    def get_hand_list(self) -> str:
        items = load_items()
        hand_desc = ""
        num = 1
        for card in self.hand:
            card = items.item_list[card]
            hand_desc += f"**{num}** {card.name} - ||{card.description}||\n"
            num += 1
        hand_desc += f"Energy: {':small_blue_diamond:'*self.combat_player.energy}"
        return hand_desc

    def get_enemy_info(self) -> str:
        pass

    def get_player_info(self) -> str:
        pass

