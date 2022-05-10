""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from helpers import checks
from rpg.player import load_player


class Inventory(commands.Cog, name="inventory-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="inventory",
        description="Shows you the contents of your inventory.",
    )
    @checks.not_blacklisted()
    async def inventory(self, interaction: ApplicationCommandInteraction):
        player = load_player(interaction.author.id)

        embed = disnake.Embed(
            title=f"{interaction.author}'s Inventory",
            description=f"Weight: {player.inventory.weight}/{player.inventory.max_weight}",
            color=0x9C84EF)
        for item, amount in player.inventory.items.items():
            # TODO: remove temp weight
            temp_weight = 3.0

            embed.add_field(
                name=f"{item} ─ {amount}",
                value=f"Weight: {round(temp_weight * amount, 1)}",
                inline=True)
        await interaction.send(embed=embed)

    @commands.slash_command(
        name="skills",
        description="Shows you all your skills and levels.",
    )
    @checks.not_blacklisted()
    async def skills(self, interaction: ApplicationCommandInteraction):
        player = load_player(interaction.author.id)

        total_lvl = 0
        for skill, lvl in player.skills.level.items():
            total_lvl += lvl

        embed = disnake.Embed(
            title=f"{interaction.author}'s Skills",
            description=f"Total Levels: {total_lvl}",
            color=0x9C84EF)

        for skill in player.skills.level:
            embed.add_field(name=f"{skill.capitalize()}",
                            value=f"LVL: {player.skills.level[skill]}    "
                                  f"XP: {player.skills.xp[skill]}/{player.skills.xp_needed[skill]}")

        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Inventory(bot))
