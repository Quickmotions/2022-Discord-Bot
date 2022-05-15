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


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="ben",
        description="This is a admin command.",
    )
    @checks.not_blacklisted()
    async def ben(self, context: Context) -> None:
        await context.send(
            "https://cdn.discordapp.com/emojis/975541799953252392.webp?size=160&quality=lossless")

    @commands.command(
        name="deeven",
        description="This is a admin command.",
    )
    @checks.not_blacklisted()
    async def deeven(self, context: Context) -> None:
        await context.send(
            "https://cdn.discordapp.com/emojis/855378824148418561.webp?size=160&quality=lossless")

    @commands.command(
        name="kerim",
        description="This is a admin command.",
    )
    @checks.not_blacklisted()
    async def kerim(self, context: Context) -> None:
        await context.send(
            "https://cdn.discordapp.com/attachments/855371424659013673/975469838900285530/IMG_1696_1.mov")

    @commands.command(
        name="harris",
        description="This is a admin command.",
    )
    @checks.not_blacklisted()
    async def harris(self, context: Context) -> None:
        await context.send(
            "https://cdn.discordapp.com/emojis/884448328534876160.webp?size=320&quality=lossless")

    @commands.command(
        name="popo",
        description="This is a admin command.",
    )
    @checks.not_blacklisted()
    async def popo(self, context: Context) -> None:
        await context.send(
            "https://cdn.discordapp.com/emojis/878306656725905448.webp?size=160&quality=lossless")

    @commands.command(
        name="kyle",
        description="This is a admin command.",
    )
    @checks.not_blacklisted()
    async def kyle(self, context: Context) -> None:
        await context.send(
            "https://cdn.discordapp.com/attachments/855371424659013673/975538897461321728/IMG-20220227-WA0008.jpg")

    @commands.command(
        name="frog",
        description="This is a admin command.",
    )
    @checks.not_blacklisted()
    async def frog(self, context: Context) -> None:
        await context.send(
            "https://cdn.discordapp.com/emojis/855772334438350848.webp?size=160&quality=lossless")

    @commands.command(
        name="rick",
        description="This is a admin command.",
    )
    @checks.not_blacklisted()
    async def rick(self, context: Context) -> None:
        await context.send(
            "https://cdn.discordapp.com/emojis/855374963719798794.gif?size=160&quality=lossless")

    @commands.command(
        name="fungus",
        description="This is a admin command.",
    )
    @checks.not_blacklisted()
    async def fungus(self, context: Context) -> None:
        await context.send(
            "https://cdn.discordapp.com/emojis/975542812311437392.webp?size=160&quality=lossless")

    @commands.command(
        name="aiden",
        description="This is a admin command.",
    )
    @checks.not_blacklisted()
    async def aiden(self, context: Context) -> None:
        await context.send(
            "https://cdn.discordapp.com/emojis/975543582649880626.webp?size=160&quality=lossless")


def setup(bot):
    bot.add_cog(Fun(bot))
