""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from discord.ext.commands import BucketType
from disnake.enums import ButtonStyle

from rpg.items import load_items
from rpg.player import load_player, save_player
from helpers import checks


class RowButtons(disnake.ui.View):
    def __init__(self, author: disnake.Member, player):
        super().__init__(timeout=None)
        self.author = author
        self.player = player

    async def interaction_check(self, inter: disnake.MessageInteraction):
        return inter.author == self.author

    @disnake.ui.button(label="Work", style=ButtonStyle.red)
    async def first_button(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        # Player gets job and base salary
        if self.player.job.job_title is None:
            self.player.job.new_job()
            embed = disnake.Embed(
                title=f"{interaction.author}'s Work Menu",
                description=f"You Started a New Job",
                color=0x9C84EF)
            embed.add_field(name=f"Job Title", value=f"{self.player.job.job_title}", inline=False)
            embed.add_field(name=f"Job Salary", value=f":moneybag: {self.player.job.salary}", inline=False)
            started_working = self.player.job.start_time.strftime("%m/%d/%Y, %H:%M:%S")
            embed.add_field(name=f"Started Working", value=f"{started_working}", inline=False)

            await interaction.response.edit_message(embed=embed)
            save_player(self.player)
            return

        # Finish work and gain salary
        amount_earned, mins_worked, promotion = self.player.job.complete_work()
        self.player.balance.change_balance(amount_earned)

        embed = disnake.Embed(
            title=f"{interaction.author}'s Work Menu",
            description=f"Finished Working",
            color=0x9C84EF)
        embed.add_field(name=f"You Earned:", value=f":moneybag: {amount_earned}", inline=False)
        embed.add_field(name=f"You Worked:", value=f"{round(mins_worked / 60, 2)} hours", inline=False)
        if promotion:
            embed.add_field(name=f"You Gained a Promotion:", value=f"New Salary: :moneybag: {self.player.job.salary}", inline=False)

        await interaction.response.edit_message(embed=embed)
        save_player(self.player)


class Work(commands.Cog, name="work-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="work",
        description="Opens the work menu",
    )
    @checks.not_blacklisted()
    async def work(self, interaction: ApplicationCommandInteraction):
        player = load_player(interaction.author.id, interaction.author.name)

        # TODO: change choice to buttons which update the embed.
        # https://docs.disnake.dev/en/latest/api.html?highlight=button#disnake.ui.Button
        embed = disnake.Embed(
            title=f"{interaction.author}'s Work Menu",
            description=f"Select an option",
            color=0x9C84EF)

        # convert job start time to readable string
        started_working = "Never"
        if player.job.start_time is not None:
            started_working = player.job.start_time.strftime("%m/%d/%Y, %H:%M:%S")

        embed.add_field(name=f"Job Title", value=f"{player.job.job_title}", inline=False)
        embed.add_field(name=f"Job Salary", value=f":moneybag: {player.job.salary}", inline=False)
        embed.add_field(name=f"Started Working", value=f"{started_working}", inline=False)

        await interaction.send(embed=embed, view=RowButtons(interaction.author, player))
        save_player(player)

    @commands.cooldown(1, 72000, BucketType.user)
    @commands.slash_command(
            name="daily",
            description="Get a daily Lootbox",
    )
    @checks.not_blacklisted()
    async def daily(self, interaction: ApplicationCommandInteraction):
        player = load_player(interaction.author.id, interaction.author.name)
        player.inventory.add_item(item="lootbox", amount=1)
        save_player(player)
        embed = disnake.Embed(
            title=f"{interaction.author}'s Daily Reward",
            description=f"You got 1x Daily Lootbox",
            color=0x9C84EF)
        await interaction.send(embed=embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Work(bot))
