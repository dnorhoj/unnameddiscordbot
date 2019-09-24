import discord
import datetime
from discord.ext import commands

async def impersonate(bot: commands.bot.Bot, message: str, user: discord.User, channel: discord.TextChannel):
    if type(channel) == int:
        channel = bot.get_channel(channel)
    if type(user) == int:
        user = bot.get_user(user)

    member = channel.guild.get_member(user.id)

    webhook = await channel.create_webhook(name=f"[HWBot] {member.name} impersonator")
    
    username = f"[HWBot] {member.display_name}"
    await webhook.send(message, username=username, avatar_url=user.avatar_url)
    await webhook.delete()