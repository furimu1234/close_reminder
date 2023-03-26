from __future__ import annotations

from discord.ext import commands
from discord import ChannelType, utils
from typing import TYPE_CHECKING
from datetime import timedelta

import yaml

if TYPE_CHECKING:
    from main import Bot
    from discord import RawThreadUpdateEvent


with open("_messages/reminder.yaml", "r", encoding="utf-8") as f:
    messages = yaml.safe_load(f)


class Close_Reminder(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_thread_update(self, payload: RawThreadUpdateEvent):
        """スレッドが更新されたら発火

        スレッドのアーカイブ期間を3日以上にしてる前提


        Parameters
        ----------
        payload : RawThreadUpdateEvent
            _description_
        """
        now = utils.utcnow()

        if not (parent := self.bot.get_channel(payload.parent_id)):
            return

        if parent.type != ChannelType.forum:
            return

        if not (thread := payload.thread):
            thread = parent.get_thread(payload.thread_id)

        # 自動アーカイブの時間が1日以内なら以降何もしない
        if thread.auto_archive_duration <= 1440:
            return

        if not thread.archived:
            return

        limit_time = utils.utcnow() + timedelta(**self.bot.limit_time)

        # スレッド作成者が投稿した一番新しいメッセージ
        last_message = [
            message
            async for message in thread.history(limit=None)
            if message.author == thread.owner
        ][0]

        # 最後に投稿されたメッセージが1日以内だったら、以降の処理をしない(手動クローズと判定)
        if last_message.created_at > limit_time:
            return

        guideline_threads = [thread for thread in parent.threads if thread.flags.pinned]

        if not guideline_threads:
            return

        guideline_thread = guideline_threads[0]

        await thread.send(
            messages["remind_message"].format(
                owner=thread.owner.mention, guideline_thread=guideline_thread.mention
            )
        )


async def setup(bot: Bot):
    await bot.add_cog(Close_Reminder(bot))
