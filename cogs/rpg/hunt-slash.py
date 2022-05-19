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

from rpg.items import load_items
from rpg.player import load_player, save_player
from rpg.combat import Combat, Enemy
from helpers import checks

hunt_locations = {"plains": "easy", "forest": "medium", "swamp": "challenging"}


class CardButton(disnake.ui.Button):

    def __init__(self, combat: Combat, label, style, disabled, custom_id):
        super().__init__(
            label=label,
            style=style,
            disabled=disabled,
            custom_id=custom_id)
        self.combat = combat

    async def callback(self, interaction: disnake.MessageInteraction):
        if interaction.author.id != self.combat.player.user_id:
            await interaction.response.send_message("This is not your combat.", delete_after=2)
            return

        items = load_items()

        card_index = int(interaction.component.custom_id[-1])
        card_id = self.combat.hand[card_index]
        if self.combat.combat_player.energy - items.item_list[card_id].cost < 0:
            await interaction.response.send_message(f"You can't use that as it costs :small_blue_diamond: "
                                                    f"{items.item_list[card_id].cost}",
                                                    delete_after=2)
            return

        self.combat.combat_player.energy -= items.item_list[card_id].cost
        self.combat.used_cards.append(interaction.component.custom_id)
        self.combat = items.use_card(card_id, self.combat)
        # end turn
        if self.combat.combat_player.energy == 0 or len(self.combat.used_cards) == len(self.combat.hand):
            self.combat.enemy_turn()
            self.combat.next_turn()

        # test winning

        winner = self.combat.check_win()
        if winner == "player":
            embed = disnake.Embed(
                title=f"{interaction.author}'s Hunt",
                description=f"Player Wins",
                color=0x9C84EF)
            await interaction.response.edit_message(embed=embed, view=None)
        elif winner == "enemy":
            embed = disnake.Embed(
                title=f"{interaction.author}'s Hunt",
                description=f"Enemy Wins",
                color=0x9C84EF)
            await interaction.response.edit_message(embed=embed, view=None)
        elif winner is None:
            # COMBAT UI
            embed = disnake.Embed(
                title=f"{interaction.author}'s Hunt",
                description=f"Pick cards until you run out of energy",
                color=0x9C84EF)
            embed.add_field(name="Player", value=self.combat.get_player_info(), inline=False)
            embed.add_field(name="Enemy", value=self.combat.get_enemy_info(), inline=False)
            embed.add_field(name="Current Hand", value=self.combat.get_hand_list(), inline=False)
            await interaction.response.edit_message(embed=embed, view=CardButtonView(interaction.author, self.combat))


class CardButtonView(disnake.ui.View):

    def __init__(self, author: disnake.Member, combat):
        super().__init__()
        self.author = author
        self.combat = combat
        self.items = load_items()
        hand: list = combat.hand
        card_num = 0
        for card in hand:
            # has card been used this turn
            if f"card_{card_num}" in combat.used_cards:
                self.add_item(CardButton(
                    label=card,
                    style=ButtonStyle.secondary,
                    disabled=True,
                    custom_id=f"card_{card_num}",
                    combat=self.combat))
            else:
                self.add_item(CardButton(
                    label=card,
                    style=ButtonStyle.secondary,
                    disabled=False,
                    custom_id=f"card_{card_num}",
                    combat=self.combat))
            card_num += 1

    async def interaction_check(self, inter: disnake.MessageInteraction):
        return inter.author == self.author


class HuntLocationDropdown(disnake.ui.Select):
    def __init__(self, author: disnake.Member, player, combat):
        self.player = player
        self.author = author
        self.combat = combat

        # Set the options that will be presented inside the dropdown
        options = []
        for option in hunt_locations:
            options.append(
                disnake.SelectOption(
                    label=option.capitalize(), description="Hunt at this location", emoji="🟥"
                )
            )

        super().__init__(
            placeholder="Choose location to hunt at",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        location = self.values[0]
        # COMBAT UI
        embed = disnake.Embed(
            title=f"{interaction.author}'s Hunt",
            description=f"You Started hunting at {location}",
            color=0x9C84EF)

        embed.add_field(name="Player", value=self.combat.get_player_info(), inline=False)
        embed.add_field(name="Enemy", value=self.combat.get_enemy_info(), inline=False)
        embed.add_field(name="Current Hand", value=self.combat.get_hand_list(), inline=False)

        # TODO: create 2 RowButtons if hand is larger than 5 don't pass combat rather pass just the hand
        await interaction.response.edit_message(embed=embed, view=CardButtonView(self.author, self.combat))


class HuntLocationDropdownView(disnake.ui.View):
    def __init__(self, author: disnake.Member, player, combat):
        super().__init__()
        self.author = author

        # Adds the dropdown to our view object.
        self.add_item(HuntLocationDropdown(author, player, combat))

    async def interaction_check(self, inter: disnake.MessageInteraction):
        return inter.author == self.author


class Hunt(commands.Cog, name="hunt-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="hunt",
        description="Opens the hunt menu",
    )
    @checks.not_blacklisted()
    async def hunt(self, interaction: ApplicationCommandInteraction):
        player = load_player(interaction.author.id, interaction.author.name)
        enemy = Enemy(name="Test Mob", location="plains", hp=100, damage=10, block=14, healing=8)
        combat = Combat(player=player, enemy=enemy)

        embed_desc = "Location Name - Difficulty:\n"
        for location, difficulty in hunt_locations.items():
            embed_desc += f"{location.capitalize()} - **{difficulty.capitalize()}**\n"

        embed = disnake.Embed(
            title=f"{interaction.author}'s Hunt Menu",
            description=embed_desc,
            color=0x9C84EF)
        await interaction.send(embed=embed, view=HuntLocationDropdownView(interaction.author, player, combat))
        save_player(player)

    # @commands.Cog.listener("on_button_click")
    # async def on_card_pick(self, interaction: disnake.MessageInteraction):
    #     if interaction.component.custom_id[:4] == "card":


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Hunt(bot))
