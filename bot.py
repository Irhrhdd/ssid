import logging
import os
import sys

import discord
from discord.ext import commands

import config  # Keep this for public API keys or constants
from views.button_one import ButtonViewOne


class PhobosBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            case_insensitive=True,
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, users=True)
        )
        self.logger = logging.getLogger("bot")

        self.admins = [767446852643192864]

    async def setup_hook(self) -> None:
        await self.load_cogs()

    async def on_ready(self):
        self.add_view(ButtonViewOne())
        self.logger.info(f"Bot connected as {self.user}")

    @staticmethod
    def setup_logging() -> None:
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.http").setLevel(logging.WARNING)
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s | %(asctime)s | %(name)s | %(message)s",
            stream=sys.stdout,
        )

    async def load_cogs(self, directory="./cogs") -> None:
        for file in os.listdir(directory):
            if file.endswith(".py") and not file.startswith("_"):
                await self.load_extension(
                    f"{directory[2:].replace('/', '.')}.{file[:-3]}"
                )
                self.logger.info(f"Loaded: {file[:-3]}")
            elif not (
                file in ["__pycache__"] or file.endswith(("pyc", "txt"))
            ) and not file.startswith("_"):
                await self.load_cogs(f"{directory}/{file}")

        await self.load_extension("jishaku")


if __name__ == "__main__":
    bot = PhobosBot()
    bot.remove_command("help")
    bot.setup_logging()

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN not set in environment variables.")
    
    bot.run(token, log_handler=None)
