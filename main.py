from __future__ import annotations

from discord.ext import commands
from discord import Intents, utils

intents = Intents.all()
intents.typing = False


class Bot(commands.Bot):
    def __init__(
        self,
        prefix: str,
        sync_tree: bool,
        extensions: tuple(str),
        limit_time: dict[str, int],
    ):
        super().__init__(command_prefix=prefix, intents=intents)

        self._extensions = extensions
        self.tree_sync = sync_tree
        self.limit_time = limit_time

    async def setup_hook(self) -> None:
        for cog in self._extensions:
            await self.load_extension(f"cogs.{cog}")

        if self.tree_sync:
            await self.tree.sync()

    async def on_ready(self):
        print("running...")
        print(str(self.user))
        print(self.user.id)
