from main import Bot
import os

extensions = ("close_reminder",)

TOKEN = os.environ.get("TOKEN")

bot = Bot(prefix="pc!", sync_tree=False, extensions=extensions)

bot.run(TOKEN)
