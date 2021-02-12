# On bot implementation, take the following scripts.
from .rolemanager import RoleManager
from .log import log

# Required to attach the Config to this particular Cog
UNIQUE_ID = 980584309543


def setup(bot):
    """
    Integrate the GBC RoleManager Extension
    """
    bot.add_cog(RoleManager(bot, UNIQUE_ID, log))
