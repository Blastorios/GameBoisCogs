from .rolemanager import RoleManager


def setup(bot):
    bot.add_cog(RoleManager())
