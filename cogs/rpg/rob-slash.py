""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""
import random

import disnake
from disnake import ApplicationCommandInteraction
from disnake.enums import ButtonStyle
from disnake.ext import commands
from discord.ext.commands import BucketType
from helpers import checks
from rpg.player import load_player, Player, save_player


class RowButtons(disnake.ui.View):
    def __init__(self, author: disnake.Member, player, target, user):
        super().__init__(timeout=None)
        self.author = author
        self.player = player
        self.target = target
        self.user = user

    async def interaction_check(self, inter: disnake.MessageInteraction):
        return inter.author == self.author

    @disnake.ui.button(label="Pickpocket", style=ButtonStyle.red)
    async def first_button(
            self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.steal(interaction, 1000)

    @disnake.ui.button(label="Burglary", style=ButtonStyle.red)
    async def second_button(
            self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.steal(interaction, 10000)

    @disnake.ui.button(label="Robbery", style=ButtonStyle.red)
    async def third_button(
            self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.steal(interaction, 75000)

    @disnake.ui.button(label="Heist", style=ButtonStyle.red)
    async def fourth_button(
            self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await self.steal(interaction, 500000)

    async def steal(self, interaction: disnake.MessageInteraction, amount):
        if self.player.balance.gold < amount:
            embed = disnake.Embed(
                title="Error!",
                description=f"You only have :moneybag: {self.player.balance.gold}",
                color=0xE02B2B
            )
            return await interaction.send(embed=embed, ephemeral=True)
        if self.target.balance.gold < amount:
            embed = disnake.Embed(
                title="Error!",
                description=f"Target only has :moneybag: {self.target.balance.gold}",
                color=0xE02B2B
            )
            return await interaction.send(embed=embed, ephemeral=True)
        # success
        if random.randint(1, 100) > 60:
            chance = random.randint(1, 100)
            if chance >= 90:
                amount_to_steal = round(amount * random.uniform(1, 1.75))
            elif chance >= 75:
                amount_to_steal = round(amount * random.uniform(1, 1.2))
            elif chance >= 50:
                amount_to_steal = round(amount * random.uniform(0.9, 1.1))
            elif chance >= 40:
                amount_to_steal = round(amount * random.uniform(0.7, 1))
            elif chance >= 30:
                amount_to_steal = round(amount * random.uniform(0.45, 1))
            elif chance >= 10:
                amount_to_steal = round(amount * random.uniform(0.3, 1))
            else:
                amount_to_steal = round(amount * random.uniform(0.1, 1))

            if amount_to_steal > self.target.balance.gold:
                amount_to_steal = self.target.balance.gold

            self.player.balance.gold += amount_to_steal
            self.target.balance.gold -= amount_to_steal

            save_player(self.player)
            save_player(self.target)
            embed = disnake.Embed(
                title=f"Successfully Robbed {self.user.name}",
                description=f"You Stole :moneybag: {amount_to_steal} from {self.user.name}",
                color=0xE02B2B
            )
            return await interaction.response.edit_message(content=f"<@{self.target.user_id}>", embed=embed, view=None)

        else:
            amount_to_pay = round(random.uniform(0.5, 1) * amount)

            self.player.balance.gold -= amount_to_pay
            self.target.balance.gold += amount_to_pay

            save_player(self.player)
            save_player(self.target)
            embed = disnake.Embed(
                title=f"Failed to Rob {self.user.name}",
                description=f"You got caught and have to pay :moneybag: {amount_to_pay} to {self.user.name}",
                color=0xE02B2B
            )
            return await interaction.response.edit_message(content=f"<@{self.target.user_id}>", embed=embed, view=None)


class Rob(commands.Cog, name="rob-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 300, BucketType.user)
    @commands.slash_command(
        name="rob",
        description="Steal from another player.",
    )
    @checks.not_blacklisted()
    async def rob(self, interaction: ApplicationCommandInteraction, user: disnake.User):
        target = load_player(user.id)
        player = load_player(interaction.author.id)

        embed = disnake.Embed(
            title=f"{interaction.author}'s Rob Menu",
            description=f"Options:\n"
                        f"----------\n"
                        f"**Pickpocket**--costs :moneybag: 1000 to plan\n"
                        f"**Burglary**-----costs :moneybag: 10000 to plan\n"
                        f"**Robbery**-----costs :moneybag: 75000 to plan\n"
                        f"**Heist**--------costs :moneybag: 500000 to plan\n",
            color=0x9C84EF)

        await interaction.response.send_message(embed=embed, view=RowButtons(interaction.author, player, target, user))


def setup(bot):
    bot.add_cog(Rob(bot))
