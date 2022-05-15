import math
import os
import pickle
import random
from datetime import datetime

from data.jobs.job_list import jobs
from rpg.items import Card


class Balance:
    def __init__(self):
        self.gold = 0

    def change_balance(self, amount: int):
        self.gold += amount


class Job:
    def __init__(self):
        self.job_title = None
        self.salary = 0
        self.start_time = None
        self.xp = 0
        self.xp_needed = 100

    def complete_work(self) -> tuple[float, int, bool]:
        start = self.start_time
        now = datetime.now()

        time_difference = now - start
        secs_worked = round(time_difference.total_seconds())
        mins_worked = round(secs_worked / 60)

        promotion = False
        salary_per_sec = self.salary / 60
        amount_earned = round(secs_worked * salary_per_sec)
        xp_earned = 0
        for _ in range(mins_worked):
            xp_earned += random.randint(1, 3)

        self.xp += xp_earned
        while self.xp >= self.xp_needed:
            self.xp -= self.xp_needed
            self.salary = self.salary + random.randint(2, 5)
            self.xp_needed = round(self.xp_needed * 1.05)
            promotion = True
        # reset work
        self.start_time = datetime.now()
        return amount_earned, mins_worked, promotion

    def new_job(self):
        self.job_title = random.choice(jobs)
        self.salary = random.randint(80, 140)
        self.start_time = datetime.now()


class Inventory:
    def __init__(self):
        self.items = {}
        self.weight = 0.0
        self.max_weight = 100.0

    def add_item(self, item: str, amount: int = 1):
        """Adds items to players inventory"""
        if item not in self.items:
            self.items[item] = 0
        self.items[item] += amount
        self.clear_empty()

    def able_remove_item(self, item: str, amount: int = 1) -> bool:
        """
        True - items were removed
        False - unable to remove items since they didn't exist
        """
        completed = False
        # does player have items
        if item in self.items and self.items[item] >= amount:
            self.items[item] -= amount
            self.clear_empty()
            completed = True
        return completed

    def clear_empty(self):
        """Removes all item keys from inventory if player has none of that item"""
        new_inv = {}
        for item, amount in self.items.items():
            if amount > 0:
                new_inv[item] = amount
        self.items = new_inv


class Skills:
    def __init__(self):
        # combat
        stats = ["health", "strength", "block", "magic", "agility",
                 "healing", "dodge", "mining", "woodcutting", "fishing"]

        self.level = {}
        self.xp = {}
        self.xp_needed = {}

        for stat in stats:
            self.level[stat] = 0
            self.xp[stat] = 0
            self.xp_needed[stat] = 100

    def add_xp(self, skill: str, amount: int):
        self.xp[skill] += amount
        while self.xp[skill] > self.xp_needed[skill]:
            self.level[skill] += 1
            self.xp[skill] -= self.xp_needed[skill]
            self.xp_needed[skill] = round(self.xp_needed[skill] * 1.2)


class Xp:
    def __init__(self):
        self.points = 0

    def add_xp(self, amount: int):
        self.points += amount


class Equipment:
    def __init__(self):
        self.slot = {
            "helmet": None,
            "chestplate": None,
            "leggings": None,
            "boots": None,
            "main_hand": None,
            "off_hand": None,
        }
        self.stats = {
            "health": 0,
            "strength": 0,
            "block": 0,
            "magic": 0,
            "agility": 0,
            "healing": 0,
            "dodge": 0,
            "mining": 0,
            "woodcutting": 0,
            "fishing": 0,
        }


class Gathering:
    def __init__(self):
        self.current = None
        self.start_time = None


class Party:
    def __init__(self):
        self.in_party = False
        self.members = {}


class Deck:
    def __init__(self):
        self.cards: dict[str:int] = {}
        self.load_starter_cards()
        self.cards_amount = len(self.cards)
        self.max_cards = 20
        self.min_cards = 10

    def load_starter_cards(self):
        for _ in range(4):
            self.cards["slash"] = 4
            self.cards["defend"] = 4
            self.cards["bash"] = 2
            self.cards["bandage"] = 1


class Player:
    def __init__(self, user_id: int, username: str):
        # user data
        self.user_id = user_id
        self.username = username
        # economy
        self.balance = Balance()

        # inventory
        self.inventory = Inventory()
        self.equipment = Equipment()

        # skills
        self.skills = Skills()
        self.xp = Xp()

        # job
        self.job = Job()

        # gathering
        self.gathering = Gathering()

        # party
        self.party = Party()

        # cards
        self.deck = Deck()

    def get_stats(self) -> dict[int]:
        """
        Calculates are returns the total active stats gained from both skill level
        and equipment stats combined
        """
        total_active_stats = {}
        for skill_name, level in self.skills.level.keys():
            # adds skill level and equipment stat level to get total skill level
            total_active_stats[skill_name] = level + self.equipment.stats[skill_name]
        return total_active_stats


def check_for_missing(player_data: Player) -> Player:
    """
    Goes through the player objects attributes and
    compares them to the default most updated player class.
    Missing attributes are then added with the default value
    """
    default_data = Player(0000, "test_player")
    # unpacks a updated default player objects attributes with default values
    for attr, value in default_data.__dict__.items():
        # if the player is missing an attribute add it with the default value
        if not hasattr(player_data, attr):
            setattr(player_data, attr, value)
        # if the attribute is a subclass then unpack this and test for missing attributes within
        if not isinstance(value, object):
            for internal_attr, internal_value in value.__dict__.items():
                # if the subclass is missing an attribute add it with the default value
                if not hasattr(getattr(player_data, attr), internal_attr):
                    setattr(getattr(player_data, attr), internal_attr, internal_value)
                # for all dictionaries inside sub classes it will check for missing keys and add them in as default
                # this will make it so that when new skills are added to the game player data will be updated
                if isinstance(internal_value, dict):

                    for dict_key, dict_value in internal_value.items():
                        if dict_key not in getattr(getattr(player_data, attr), internal_attr):
                            # add a new key with default value into the sub-classes dictionary
                            getattr(getattr(player_data, attr), internal_attr)[dict_key] = dict_value
    return player_data


def load_player(user_id: int, username: str) -> Player:
    """creates a default player data if missing, then loads the player data for specified user_id"""

    if not player_exists(user_id):
        register_user(user_id, username)
    with open(f"data/players/{user_id}/player_data.pkl", "rb") as pickle_file:
        player = pickle.load(pickle_file)
        player = check_for_missing(player)
        return player


def load_all_players() -> list[Player]:
    """creates a default player data if missing, then loads the player data for specified user_id"""
    players = []
    for user_id in os.listdir("data/players/"):
        with open(f"data/players/{user_id}/player_data.pkl", "rb") as pickle_file:
            player = pickle.load(pickle_file)
            players.append(player)
    return players


def save_player(player_data: Player):
    with open(f"data/players/{player_data.user_id}/player_data.pkl", "wb") as pickle_file:
        pickle.dump(player_data, pickle_file)


def register_user(user_id: int, username: str):
    """
    registers a new player and creates default data for them then stores it in pickle file
    """
    if not player_exists(user_id):
        os.makedirs(f"data/players/{user_id}")
        player_data = Player(user_id, username)
        # create and save pickle file
        with open(f"data/players/{user_id}/player_data.pkl", "wb") as pickle_file:
            pickle.dump(player_data, pickle_file)


def player_exists(user_id: int) -> bool:
    """tests if a specified user_id exists in data"""
    if os.path.exists(f"data/players/{user_id}"):
        return True
    return False
