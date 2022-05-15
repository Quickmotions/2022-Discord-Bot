""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

from disnake.ext import commands
from disnake.ext.commands import Context

from helpers import checks
from rpg.items import load_items, save_items, Card, Material, Equipment


class Admin(commands.Cog, name="admin-normal"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="addmaterial",
        description="This is a admin command.",
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def addmaterial(self, context: Context, id: str, name: str, description: str) -> None:
        items = load_items()
        items.add(Material(id, name, description))
        await context.reply("added item")
        save_items(items)

    @commands.command(
        name="addequipment",
        description="This is a admin command.",
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def addequipment(self, context: Context, id: str, name: str, description: str, slot: str, armor: int) -> None:
        items = load_items()
        items.add(Equipment(id, name, description, slot, armor))
        await context.reply("added item")
        save_items(items)

    @commands.command(
        name="addcard",
        description="This is a admin command.",
    )
    @checks.not_blacklisted()
    @checks.is_owner()
    async def addcard(self, context: Context, id: str, name: str, description: str, card_type: str,
                      rarity: str,
                      cost: int = 1,
                      exhaust: str = "False",
                      unique: str = "False",
                      damage: int = 0,
                      healing: int = 0,
                      block: int = 0,
                      skill_type: str = None,
                      effect: str = None) -> None:
        items = load_items()
        if exhaust == "False":
            exhaust = False
        if unique == "False":
            unique = False
        items.add(Card(id, name, description, card_type, rarity, cost, exhaust, unique, damage,
                       healing, block, skill_type, effect))
        await context.reply("added item")
        save_items(items)


def setup(bot):
    bot.add_cog(Admin(bot))
