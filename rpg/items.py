import os
import pickle


class Item:
    def __init__(self, id: str, name: str, category: str, description: str):
        """
        :param id: short-form string id given to all items
        :param name: name of item
        :param category: used for sorting items. eg. "cards", "equipment", "material"
        :param description: short description of item
        """
        self.id = id
        self.name = name
        self.category = category
        self.description = description


class Card(Item):
    def __init__(self, id: str, name: str, description: str, card_type: str, rarity: str, cost: int = 1,
                 exhaust: bool = False, unique: bool = False, damage: int = 0, healing: int = 0, block: int = 0,
                 skill_type: str = None, effect: str = None):
        """
        :param card_type: "attack", "skill", "power", "status"
        :param rarity: "common", "uncommon", "rare", "legendary", "ascended"
        :param cost: how many points to cast in battle
        :param exhaust: if the card is removed for rest of battle after use
        :param unique: if player may have more than 1 of this card in their deck
        :param damage: damage caused to enemy on use
        :param healing: healing caused to player on use
        :param block: block applied to player on use
        :param skill_type: what skill (i.e. magic, defense) all effects of card are multiplied by
        :param effect: custom effect string must be added separately in the Card class
        """
        super().__init__(id=id, name=name, category="cards", description=description)
        self.card_type: str = card_type
        self.rarity: str = rarity
        self.cost: int = cost
        self.exhaust: bool = exhaust
        self.unique: bool = unique
        self.damage: int = damage
        self.healing: int = healing
        self.block: int = block
        self.skill_type: str = skill_type

        # card effects
        if effect == "example_effect":
            self.effect = self.example_effect

    def example_effect(self):
        # perform special thing in combat here.
        # eg. duplicate a random card in players hand
        pass


class Equipment(Item):
    def __init__(self, id: str, name: str, description: str, slot: str, armor: int = 0, stats: dict = None):
        """
        :param slot: "head", "chest", "legs", "feet", "main-hand", "off-hand"
        :param armor: percentage of damage reduction from this item
        :param stats: dict of stats which are changed, eg. {"strength": -1, "magic": 4}
        """
        super().__init__(id=id, name=name, category="equipment", description=description)
        if stats is None:
            stats = {}
        self.slot: str = slot
        self.armor: int = armor
        self.stats_to_increase: dict = stats


class Material(Item):
    def __init__(self, id: str, name: str, description: str):
        super().__init__(id=id, name=name, category="materials", description=description)


class ItemManager:
    def __init__(self):
        self.item_list = {}

    def add(self, item: Item):
        self.item_list[item.id] = item

    def use_card(self, card_id: str, combat):
        skill_modifier = 0.15  # 15% more stat per lvl
        card = self.item_list[card_id]
        if card.card_type == "attack":
            print(card.damage)
            combat.enemy.take_damage(round(card.damage * (1 + (skill_modifier * combat.combat_player.skill_strength))))
            combat.combat_player.block += round(card.block * (1 + (skill_modifier * combat.combat_player.skill_block)))
            combat.combat_player.hp += round(card.healing * (1 + (skill_modifier * combat.combat_player.skill_healing)))
            if combat.combat_player.hp > combat.combat_player.hp_max:
                combat.combat_player.hp = combat.combat_player.hp_max
        return combat


def load_items() -> ItemManager:
    items = ItemManager()
    for category in os.listdir(f"{os.getcwd()}\data\items"):
        for pkl_item in os.listdir(f"{os.getcwd()}\data\items\{category}"):
            with open(f"data/items/{category}/{pkl_item}", "rb") as pickle_file:
                item = pickle.load(pickle_file)
                items.add(item)
    return items


def save_items(item_manager: ItemManager):
    for item_id, item in item_manager.item_list.items():
        with open(f"data/items/{item.category}/{item.id}.pkl", "wb") as pickle_file:
            pickle.dump(item, pickle_file)
