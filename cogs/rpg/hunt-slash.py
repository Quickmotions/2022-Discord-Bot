""""
Copyright © Krypton 2022 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
This is a template to create your own discord bot in python.

Version: 4.1
"""

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.enums import ButtonStyle
from disnake.ui import Button

from rpg.player import load_player, save_player
from rpg.combat import Combat
from helpers import checks

hunt_locations = {"plains": "easy", "forest": "medium", "swamp": "challenging"}

async def generate_rows(bot: lightbulb.BotApp) -> t.Iterable[ActionRowBuilder]:
    """Generate 2 action rows with 4 buttons each."""

    # This will hold our action rows of buttons. The limit
    # imposed by Discord is 5 rows with 5 buttons each. We
    # will not use that many here, however.
    rows: t.List[ActionRowBuilder] = []

    # Build the first action row
    row = bot.rest.build_action_row()

    # Here we iterate len(COLORS) times.
    for i in range(len(COLORS)):
        if i % 4 == 0 and i != 0:
            # If i is evenly divided by 4, and not 0 we want to
            # append the first row to rows and build the second
            # action row. (Gives a more even button layout)
            rows.append(row)
            row = bot.rest.build_action_row()

        # Extract the current color from the mapping and assign
        # to this label var for later.
        label = list(COLORS)[i]

        # We use an enclosing scope here so that we can easily chain
        # method calls of the action row.
        (
            # Adding the buttons into the action row.
            row.add_button(
                # Gray button style, see also PRIMARY, and DANGER.
                hikari.ButtonStyle.SECONDARY,
                # Set the buttons custom ID to the label.
                label,
            )
            # Set the actual label.
            .set_label(label)
            # Finally add the button to the container.
            .add_to_container()
        )

    # Append the second action row to rows after the for loop.
    rows.append(row)

    # Return the action rows from the function.
    return rows



class HuntLocationDropdown(disnake.ui.Select):
    def __init__(self, author: disnake.Member, player):
        self.player = player
        self.author = author

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
        embed = disnake.Embed(
            title=f"{interaction.author}'s Hunt",
            description=f"You Started hunting at {location}",
            color=0x9C84EF)
        enemy = None
        combat = Combat(player=self.player, enemy=None)
        embed.add_field(name="Current Hand", value=combat.get_hand_list())

        await interaction.response.edit_message(embed=embed, view=None)


class HuntLocationDropdownView(disnake.ui.View):
    def __init__(self, author: disnake.Member, player):
        super().__init__()
        self.author = author

        # Adds the dropdown to our view object.
        self.add_item(HuntLocationDropdown(author, player))

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
        player = load_player(interaction.author.id)

        embed_desc = "Location Name - Difficulty:\n"
        for location, difficulty in hunt_locations.items():
            embed_desc += f"{location.capitalize()} - **{difficulty.capitalize()}**\n"

        embed = disnake.Embed(
            title=f"{interaction.author}'s Hunt Menu",
            description=embed_desc,
            color=0x9C84EF)
        await interaction.send(embed=embed, view=HuntLocationDropdownView(interaction.author, player))
        save_player(player)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Hunt(bot))
