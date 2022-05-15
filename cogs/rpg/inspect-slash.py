""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""
import random

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from rpg.items import load_items
from helpers import checks
from rpg.player import load_player, save_player


class Inspect(commands.Cog, name="inspect-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="inspect",
        description="Tells you information about an item",
    )
    @checks.not_blacklisted()
    async def work(self, interaction: ApplicationCommandInteraction, item_id: str):
        items = load_items()
        item_id = item_id.lower()
        if item_id in items.item_list:
            embed = disnake.Embed(
                title=f"{items.item_list[item_id].name}",
                description=f"{items.item_list[item_id].description}",
                color=0x9C84EF)
            embed.add_field(name="Category", value=f"{items.item_list[item_id].category.capitalize()}")
        else:
            embed = disnake.Embed(
                title=f"Inspect Failed",
                description=f"Couldn't find item with item id: {item_id}",
                color=0x9C84EF)
        await interaction.response.send_message(embed=embed)

    @commands.slash_command(
        name="use",
        description="Use an item",
    )
    @checks.not_blacklisted()
    async def use(self, interaction: ApplicationCommandInteraction, item_id: str):
        items = load_items()
        player = load_player(interaction.author.id)
        if item_id == "lootbox":
            if not player.inventory.able_remove_item("lootbox", 1):
                embed = disnake.Embed(
                    title=f"Error Using {items.item_list[item_id].name}",
                    description=f"You don't own any {items.item_list[item_id].name}",
                    color=0x9C84EF)
                await interaction.response.send_message(embed=embed)
                return

            chance = random.randint(1, 100)
            print(chance)
            coins = 0
            if chance >= 80:
                coins += random.randint(50000, 100000)
            if chance >= 50:
                coins += random.randint(10000, 20000)
            if chance >= 20:
                coins += random.randint(5000, 15000)
            if chance >= 10:
                coins += random.randint(1000, 2500)
            else:
                coins += random.randint(1, 100)
            player.balance.change_balance(amount=coins)
            save_player(player)

            embed = disnake.Embed(
                title=f"Using {items.item_list[item_id].name}",
                description=f"You got :moneybag: {coins}",
                color=0x9C84EF)
            await interaction.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(
                title=f"Use Command Failed",
                description=f"Couldn't find item with item id: {item_id}",
                color=0x9C84EF)
            await interaction.response.send_message(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Inspect(bot))
