'''Simple Role Manager
Created on: 18/01/2021
Created by: @Blastorios'''

import json
from pathlib import Path
from typing import Tuple, Optional

import discord
from redbot.core import checks, commands
from redbot.core.data_manager import cog_data_path

# TODO
# Initialize a JSON file within the data dir to store user-acquired roles
# Create a 'on-cog-startup (aka method called inside init)' method to insert the JSON storage if it can find anything at the predetermined data dir
# Make a Simple update function that allows the cog to check all added roles within the data


class RoleManager(commands.Cog):
    """
    Straightforward Role Generator with the use of emojis
    """

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.set_message_att = {
            "presence": False,
            "message": "",
            "message_id": ""
        }
        self.emoji_to_role = {}
        self._set_persistent_data()

    def _set_persistent_data(self):
        """
        ALlow for persisent Role Management when the bot gets disconnected and/or the VPS goes offline.
        """
        self.data_position = cog_data_path(
            raw_name="RoleManager") / "rolemanager_storage.json"

        if self.data_position.is_file():
            return

        new_json_data = {
            "members": {},
            "banned members": {},
            "emoji_to_role": {},
        }

        try:
            with open(self.data_position, "r") as data_container:
                json.dump(new_json_data, data_container)
        except IOError:
            return f"""
            Could not open Storage Container at filepath {self.data_position}.
            """
        return

    async def _check_payload_message(self, payload) -> Tuple:
        if self.set_message_att["message_id"] or payload.message_id != self.set_message_att["message_id"]:
            # If the setmessage has not been used yet || the payload id doesnt match the setmessage id
            return False

        try:
            role_id = self.emoji_to_role[payload.emoji]
            # Check whether the role is even within the available options (prevent arbitrary spam)
        except KeyError:
            return False

        guild = self.get_guild(payload.guild_id)
        role = guild.get_role(role_id)

        if guild is None or role is None:
            # When the bot cant find a reasonable guild or role
            return False

        return guild, role

    @bot.event
    async def on_raw_reaction_add(self, payload):
        """
        On the event of a user adding a reaction to the specified message: add specified role

        :params:

        """
        parsed = await self._check_payload_message(payload)

        if parsed:
            try:
                await payload.member.add_roles(parsed[-1])
            except discord.HTTPException:
                payload.member.send(
                    f"Unable to add role {parsed[-1]}. Please contact a mod for help.")

    @bot.event
    async def on_raw_reaction_remove(self, payload):
        """
        On the event of a user removing a reaction from the specified message: remove specified role
        """
        pass

    @checks.admin_or_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.guild_only()
    @commands.command(name="setmessage")
    async def setmessage(self, ctx: commands.GuildContext, message: str):
        """
        Set the message to add the emoji's
        """
        if self.set_message_att["presence"]:
            return await ctx.send("A Message has already been set for this server. Use '-newmessage' to change it")

        send_message = await ctx.send(f"{message}")
        self.set_message_id = send_message.id

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
