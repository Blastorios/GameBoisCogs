'''Simple Role Manager
Created on: 18/01/2021
Created by: @Blastorios'''

import json
import string
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import discord
from redbot.core import checks, commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core.commands import GuildContext
from redbot.core.data_manager import cog_data_path

from .log import log
from .get_class_atts import get_class_attributes


class RoleManager(commands.Cog):
    """
    Gamebois RoleManager. 

    Designed to contain all necessary Role Management Functionalities.

    :params:

    bot: The Redbot Core

    return RoleManager object
    """

    __author__ = "Blastorios"
    __credits__ = ["Blastorios"]

    __license__ = "MIT"
    __version__ = "0.1.0"
    __maintainer__ = "Blastorios"
    __status__ = "Development"

    def __init__(self, bot, unique_id, logs):
        super().__init__()
        self.bot = bot
        self._config = Config.get_conf(
            self, identifier=unique_id, force_registration=True)

        self._config.register_guild(
            roles={},
            welcome_message="",
            welcome_message_id="",
            welcome_message_channel="",
        )

        self._cached = Dict()

        # self._config.register_member(
        #     trusted=False,
        #     roles=[],
        #     forbidden=[],
        # )

        # self._config.register_role(
        #     emoji="",
        #     requires=[]
        # )

    @checks.admin_or_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.command(name="setmessage")
    async def setmessage(self, ctx: commands.GuildContext, message: str):
        """
        Set the message to add the emoji's
        """
        guild = ctx.message.guild
        current_message = await self._config.guild(guild).welcome_message()

        # Check if the guild alrdy has used 'setmessage'
        if current_message:
            await ctx.send("A Message has already been set for this server. Would you like to change it? (respond with yes or no)")
            continue_setup = await bot.wait_for(
                'message', check=lambda message: message if message.author == ctx.author and message.channel in guild.channels and (message.lower() == "yes" or message.lower() == "no"))
            if continue_setup.lower() == "yes":
                pass
            else:
                return await ctx.send("Stopped the setup")

        # Intermediate Update about the progress
        ctx.send("""
        Succesfully received the new message for RoleManager!
        
        Which channel would you like to post it? (Type the exact channel name in chat)
        """)

        # Simple watcher
        which_channel = await bot.wait_for(
            'message', check=lambda message: message if message.author == ctx.author and message.channel in guild.channels else False)

        if not which_channel:
            return
        # Create try/except blocks to check for assignment availability
        try:
            assigned_channel = discord.utils.get(
                ctx.guild.channels, name=which_channel)

        except Exception as exc:
            return await ctx.send(f"Could not find channel {which_channel}. Encountered error: {exc}")

        try:
            await self._config.guild(guild).welcome_message.set(message)
            await self._config.guild(guild).welcome_message_channel.set(assigned_channel.id)

        except Exception as exc:
            return await ctx.send(f"Could not assign given content to {guild} guild Configuration. Encountered Error: {exc}")

        # Purposely taking the message from the Config object for persistence.
        return await assigned_channel.send(self._config.guild(guild).welcome_message())

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        On the event of a user adding a reaction to the specified message: add specified role

        :params:

        """
        guild = payload.guild

        try:
            await payload.member.add_roles(parsed[-1])
        except discord.HTTPException:
            payload.member.send(
                f"Unable to add role {parsed[-1]}. Please contact a mod for help.")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """
        On the event of a user removing a reaction from the specified message: remove specified role
        """
        pass

    @checks.admin_or_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.guild_only()
    @commands.command(name="setemojis")
    async def setemojis(self, ctx: commands.GuildContext, emoji: str, role: str):
        """
        Link an emoji to its respective role
        """

        try:
            self.emoji_to_role[f"{emoji}"] = f"{role}"
        except Exception as e:
            await ctx.author.send(f"Could not link given emoji to given role. Encountered: {e}")

    @checks.admin_or_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.guild_only()
    @commands.command(name="newmessage")
    async def newmessage(self, ctx: commands.GuildContext, message: str):
        """
        Edit the message to add the emoji's
        """
        if not self.set_message_att["presence"]:
            try:
                self.set_message_att["message_id"]
        send_message = await ctx.send(f"{message}")
        self.set_message_id = send_message.id
