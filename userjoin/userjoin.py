from typing import Tuple, Optional

import discord
from redbot.core import checks, commands


class UserJoin(discord.Client):
    """
    A simple on_member_join cog
    """

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.welcome_message = ""
        self.second_chance = None

    @checks.admin_or_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.guild_only()
    @commands.command(name="setwelcome")
    async def setwelcome(self, ctx, message: str):
        """
        Allows the user to set a welcome message interactively.
        """

        self.welcome_message = f"""
        {message}

        Press 🟢 to accept or 🔴 to decline.
        """

    @bot.event
    async def on_member_join(self, member: discord.Member):
        """
        Event hook to send a simple private message with responder.
        """

        message_to_send = self.welcome_message if not self.welcome_message else "Welcome to the server! Be sure to follow general rules and introduce yourself in the general chat!"

        created_dm_channel = await member.create_dm()
        interactive_message = await created_dm_channel.send(message_to_send)

        for welcome_emoji in ["🟢", "🔴"]:
            try:
                await interactive_message.add_reaction(welcome_emoji)
            except:
                return "Failed to add reactive emojis on welcome message."

        def valid_emoji(reaction, user):
            return user == member and str(reaction.emoji) == "🟢"

        try:
            reaction, user = await bot.wait_for('reaction_add', check=valid_emoji)
        except:
            await created_dm_channel.send(
                'Something went wrong? Please contact the server owner!')

        if reaction == "🟢":
            await created_dm_channel.send("Good Choice 😊, you're an official GameBois member now! See you soon!")
            await member.add_roles("Member")
        else:
            self.second_chance = await created_dm_channel.send("""
            That hurts.. 😔, but your choice! Best of luck in the wildlands of Discord.
            
            If you ever change your mind and do accept, react to this message with a "🟢" emoji to get into the server!
            """)

    @bot.event
    async def on_raw_reaction_add(self, payload):
        """
        An 'after-math' for people to reconsider their 'decision.'
        """
        if self.second_chance != None:
            if payload.message_id == self.second_chance.message_id:
                if payload.emoji == "🟢":
                    await payload.member.create_dm().send("I am glad to see you reconsidered!")
                    await payload.member.add_roles("Member")
        return
