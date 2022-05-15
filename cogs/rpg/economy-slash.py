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

# Here we name the cog and create a new class for the cog.
from rpg.player import load_player, save_player, load_all_players


class Economy(commands.Cog, name="economy-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="bal",
        description="Check a players balance.",
    )
    @checks.not_blacklisted()
    async def bal(self, interaction: ApplicationCommandInteraction, user: disnake.User = None):
        """
        Displays the specified users balance.
        If no user is selected user is defaulted to user who send the
        """
        if user is None:
            user = interaction.user

        player = load_player(user.id, user.name)

        embed = disnake.Embed(
            title=f"{user.name}'s Balance",
            description=f":moneybag: {player.balance.gold}",
            color=0x9C84EF)
        await interaction.response.send_message(embed=embed)
        save_player(player)

    @commands.slash_command(
        name="pay",
        description="Pay another player.",
    )
    @checks.not_blacklisted()
    async def pay(self, interaction: ApplicationCommandInteraction, user: disnake.User, amount: int):
        player = load_player(interaction.author.id, interaction.author.name)
        target = load_player(user.id, user.name)

        failure = None
        if amount <= 0:
            failure = f"Amount must be greater than :moneybag: 0"

        if player.balance.gold < amount:
            failure = f"You only have :moneybag: {player.balance.gold}"

        # On failure send failure as message and cancel command
        if failure is not None:
            embed = disnake.Embed(
                title=f"Failed to pay {user.name}",
                description=failure,
                color=0x9C84EF)
            await interaction.send(embed=embed)
            return

        # Command Worked

        player.balance.change_balance(amount=-amount)
        target.balance.change_balance(amount=amount)
        embed = disnake.Embed(
            title=f"Payed {user.name}",
            description=f":moneybag: {amount}",
            color=0x9C84EF)
        embed.add_field(name=f"{user.name} (+{amount})",
                        value=f"Balance: :moneybag: {target.balance.gold}",
                        inline=False)
        embed.add_field(name=f"{interaction.author.name} (-{amount})",
                        value=f"Balance: :moneybag: {player.balance.gold}",
                        inline=False)

        await interaction.send(embed=embed)
        save_player(player)
        save_player(target)

    @commands.slash_command(
        name="baltop",
        description="Lists the richest players",
    )
    @checks.not_blacklisted()
    async def baltop(self, interaction: ApplicationCommandInteraction):
        players = load_all_players()
        player_bal = []
        for player in players:
            player_bal.append([player.username, player.balance.gold])
        player_bal.sort(key=lambda x: x[1], reverse=True)
        baltop_desc = ""
        pages = []
        array = 0
        num = 1
        for username, bal in player_bal:
            if array == 9:
                array = 0
                pages.append(baltop_desc)
                baltop_desc = ""
            baltop_desc += f"**{num}** `{bal}` - {username}\n"
            array += 1
            num += 1
        pages.append(baltop_desc)
        # TODO: add paginator to show more pages of bal top listed in pages[]
        embed = disnake.Embed(
            title=f"Richest Users",
            description=pages[0],
            color=0x9C84EF)
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
