import disnake
import random

from rpg.player import Player
from rpg.items import load_items


class PlayerCombat:
    def __init__(self, player: Player):
        self.user_id: int = player.user_id
        self.player = player

        # skills
        self.skill_health = player.skills.level["health"]
        self.skill_strength = player.skills.level["strength"]
        self.skill_block = player.skills.level["block"]
        self.skill_magic = player.skills.level["magic"]
        self.skill_agility = player.skills.level["agility"]
        self.skill_healing = player.skills.level["healing"]
        self.skill_dodge = player.skills.level["dodge"]

        self.hp_max: int = round(((self.skill_health * 0.15) + 1) * 20)  # 15% for every lvl of health
        self.hp: int = self.hp_max
        self.energy_max: int = 3
        self.energy: int = self.energy_max
        self.block = 0

        # cards
        self.deck = player.deck
        self.discard = {}

        self.gained_gold: int = 0
        self.gained_xp: int = 0

    def draw_hand(self, hand_size: int = 5):
        """
        :hand: a list of :param hand_size: cards
        :self.deck.cards: full deck
        :self.discard: dict of cards to remove from deck
        """
        hand = []
        for _ in range(hand_size):
            deck = self.deck_list()
            if len(deck) == 0:
                # reshuffle discard back into deck
                self.discard = {}
                deck = self.deck_list()
            # select a random card from current deck
            random_card = random.choice(deck)
            # add selected card into discard
            if random_card not in self.discard:
                self.discard[random_card] = 0
            self.discard[random_card] += 1

            hand.append(random_card)
        return hand

    def deck_list(self) -> list[str]:
        """returns a list of card id in deck with discarded cards removed"""
        deck = []
        for card, amount in self.deck.cards.items():
            for _ in range(amount):
                deck.append(card)
        for card, amount in self.discard.items():
            for _ in range(amount):
                deck.remove(card)
        return deck

    def take_damage(self, damage: int):
        block_left = self.block - damage
        if block_left > 0:
            self.block -= damage
        else:
            damage = damage - self.block
            self.block = 0
            self.hp -= damage


class Enemy:
    def __init__(self, name: str = "Mob", location: str = "plains", hp: int = 1,
                 damage: int = 0, block: int = 0, healing: int = 0, loot=None):
        if loot is None:
            loot = {}

        self.name = name
        self.hp_max = hp
        self.hp = self.hp_max
        self.damage = damage
        self.block = block
        self.current_block = 0
        self.healing = healing
        self.location = location
        self.loot = loot
        self.options = []
        if self.damage > 0:
            self.options.append("damage")
        if self.block > 0:
            self.options.append("block")
        if self.healing > 0:
            self.options.append("healing")

        self.next_attack = random.choice(self.options)

    def take_damage(self, damage: int):
        block_left = self.current_block - damage
        if block_left > 0:
            self.current_block -= damage
        else:
            damage = damage - self.current_block
            self.current_block = 0
            self.hp -= damage

    def pick_attack(self):
        self.next_attack = random.choice(self.options)


class Combat:
    def __init__(self, player: Player, enemy: Enemy):
        self.combat_player = PlayerCombat(player)
        self.player = player
        self.enemy = enemy
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

    def enemy_turn(self):
        self.enemy.current_block = 0

        if self.enemy.next_attack == "damage":
            self.combat_player.take_damage(self.enemy.damage)
        if self.enemy.next_attack == "healing":
            self.enemy.hp += self.enemy.healing
            if self.enemy.hp > self.enemy.hp_max:
                self.enemy.hp = self.enemy.hp_max
        if self.enemy.next_attack == "block":
            self.enemy.current_block = self.enemy.block

        self.enemy.pick_attack()

    def get_hand_list(self) -> str:
        items = load_items()
        hand_desc = ""
        num = 1
        for card in self.hand:
            card = items.item_list[card]
            hand_desc += f"**{num}** {card.name} - ||{card.description}||\n"
            num += 1
        hand_desc += f"Energy: {':small_blue_diamond:' * self.combat_player.energy}"
        return hand_desc

    def get_enemy_info(self) -> str:
        if self.enemy.next_attack == "damage":
            attack = f":crossed_swords: Deal {self.enemy.damage} damage"
        elif self.enemy.next_attack == "block":
            attack = f":shield: Block {self.enemy.block} damage"
        elif self.enemy.next_attack == "healing":
            attack = f":mending_heart: Heal {self.enemy.healing} hp"
        else:
            attack = f"Nothing"

        return f"--------- *{self.enemy.name}* --------- :shield: {self.enemy.current_block}\n" \
               f"{create_hp_bar(self.enemy.hp, self.enemy.hp_max)}\n" \
               f"--------- *Next Attack* ---------\n" \
               f"{attack}"

    def get_player_info(self) -> str:
        return f"--------- *{self.player.username}* --------- :shield: {self.combat_player.block}\n" \
               f"{create_hp_bar(self.combat_player.hp, self.combat_player.hp_max)}"

    def check_win(self):
        if self.combat_player.hp <= 0:
            return "enemy"
        if self.enemy.hp <= 0:
            return "player"
        return None


def create_hp_bar(hp, hp_max) -> str:
    red = round(hp / hp_max * 10)
    white = 10 - red
    return f"{':red_square:' * red}{':black_large_square:' * white} ({hp})"
