from main import Bot
import os

extensions = ("close_reminder",)

TOKEN = os.environ.get("TOKEN")

bot = Bot(prefix=".", sync_tree=False, extensions=extensions, limit_time={"days": 1})

bot.run(TOKEN)
