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
from disnake.enums import ButtonStyle

from helpers import checks
from rpg.player import load_player, save_player


# TODO: clean this coin flips button system up so that there isn't the same thing happening 4 times
class RowButtons(disnake.ui.View):
    def __init__(self, author: disnake.Member, player, amount):
        super().__init__(timeout=None)
        self.author = author
        self.player = player
        self.amount = amount

    async def interaction_check(self, inter: disnake.MessageInteraction):
        return inter.author == self.author

    @disnake.ui.button(label="Heads", style=ButtonStyle.blurple)
    async def first_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        # Heads
        if random.randint(1, 2) == 1:
            embed = disnake.Embed(
                title=f"{interaction.author}'s Coinflip",
                description=f"Heads was flipped!!!\n"
                            f"You get :moneybag: {self.amount}",
                color=0x9C84EF)
            self.player.balance.gold += self.amount
        else:
            embed = disnake.Embed(
                title=f"{interaction.author}'s Coinflip",
                description=f"Tails was flipped...\n"
                            f"You lost :moneybag: {self.amount}",
                color=0x9C84EF)
            self.player.balance.gold -= self.amount

        button.disabled = True

        await interaction.response.edit_message(embed=embed, view=None)
        save_player(self.player)

    @disnake.ui.button(label="Tails", style=ButtonStyle.green)
    async def second_button(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        # Tails
        if random.randint(1, 2) == 1:
            embed = disnake.Embed(
                title=f"{interaction.author}'s Coinflip",
                description=f"Tails was flipped!!!\n"
                            f"You get :moneybag: {self.amount}",
                color=0x9C84EF)
            self.player.balance.gold += self.amount
        else:
            embed = disnake.Embed(
                title=f"{interaction.author}'s Coinflip",
                description=f"Heads was flipped...\n"
                            f"You lost :moneybag: {self.amount}",
                color=0x9C84EF)
            self.player.balance.gold -= self.amount

        button.disabled = True

        await interaction.response.edit_message(embed=embed, view=None)
        save_player(self.player)


class Gamble(commands.Cog, name="gamble-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="coinflip",
        description="Flip a coin gamble some money",
    )
    @checks.not_blacklisted()
    async def coinflip(self, interaction: ApplicationCommandInteraction, amount: int):
        player = load_player(interaction.author.id)

        failure = None
        if amount <= 0:
            failure = f"Amount must be greater than :moneybag: 0"

        if player.balance.gold < amount:
            failure = f"You tried to gamble {amount} but only have {player.balance.gold}"

        if amount > 50000:
            failure = f"The maximum amount you are allowed to flip for is :moneybag: 50000"

        # On failure send failure as message and cancel command
        if failure is not None:
            embed = disnake.Embed(
                title=f"Failed to Coinflip",
                description=failure,
                color=0x9C84EF)
            await interaction.send(embed=embed)
            return

        # Command Worked
        embed = disnake.Embed(
            title=f"{interaction.author}'s Coinflip",
            description=f"You are attempting to gamble :moneybag: {amount}\n"
                        f"Pick heads or tails below",
            color=0x9C84EF)

        await interaction.send(embed=embed, view=RowButtons(interaction.author, player, amount))


def setup(bot):
    bot.add_cog(Gamble(bot))
