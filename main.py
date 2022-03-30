from os import listdir
from discord import Embed, Colour, Intents
from discord.ext import commands


def errorembed(error: str):
    embed = Embed(
        title="An error occurred",
        description=error,
        colour=Colour.red()
    )
    return embed



class BadFlagError(NameError):
    """Base class for all flag related errors"""
    def __init__(self, override_message: str = None):
        if override_message is None:
            self._message = "One or more flags in the command is invalid"
        else:
            self._message = override_message
        super().__init__(self._message)


class MissingRequiredFlagError(BadFlagError):
    """Raised when a required flag is missing from a command"""
    def __init__(self, override: str = None):
        if override is None:
            self._message = "Missing a required flag"
        else:
            self._message = override
        super().__init__(self._message)


def flagsparse(flags: tuple, defaults: dict) -> dict:
    """Parses a list of flags against a dict of flags and returns the output"""
    for flag in flags:
        if "=" in flag:
            args = flag.split("=")
            argsearch = defaults.get(args[0])
            if argsearch is None:  # Either the flag doesn't exist or doesn't take an arg, raise an error
                raise BadFlagError()
            else:
                defaults[args[0]] = args[1]
        else:
            search = defaults.get(flag)
            if search is None:  # User supplied a flag that does not exist, return an error
                raise BadFlagError()
            else:
                defaults[flag] = True
    return defaults


generic_403 = Embed(
    title="Access Denied",
    description="You're not authorized to use this command",
    color=Colour.red()
)
tim = commands.Bot(commands_prefix="tim", intents=Intents.all(), case_insensitive=True)
tim.generic_403 = generic_403
tim.BadFlagError = BadFlagError
tim.MissingRequiredFlagError = MissingRequiredFlagError
tim.flagsparse = flagsparse


@tim.event
def on_ready():
    print("Ready to complain about OTS details")


@tim.command(name="reload-cogs", hidden=True)
async def ext_reload(ctx: commands.Context, *flags):
    default = {
        "--all": False,
        "--cog": ""
    }
    settings = flagsparse(flags, default)
    if settings["--all"] is None and settings["--cog"] == "":
        raise MissingRequiredFlagError()
    elif settings["--all"] is True:
        for file in listdir("cogs"):
            tim.reload_extension(f"cogs.{file.rstrip('.py')}")
    else:
        cog = settings["--cog"]
        try:
            tim.reload_extension(f"cogs.{cog}")
        except commands.ExtensionNotFound:
            error = errorembed("Could not find that extension")
            await ctx.send(embed=error)
