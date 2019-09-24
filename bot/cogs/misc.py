import discord
from discord.ext import commands
import utils
import json

class Misc(commands.Cog):
	"""Miscellaneous commands"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden=True)
	@commands.check(lambda ctx: ctx.message.author.id == 281409966579908608)
	async def fix(self, ctx, msgid: int):
		await ctx.message.delete()

		fix_dict = json.load(open("config/fix.json", "r"))

		try:
			message = await ctx.channel.fetch_message(msgid)
		except discord.errors.NotFound:
			await ctx.author.send(f"Der findes ikke nogen beskeder med idet `{str(msgid)}``")
		message_id = str(message.channel.id)

		target_channel = fix_dict.get(message_id)
		if target_channel is None:
			await ctx.author.send(f"Kanalen `{ctx.channel.name}` er ikke programmeret ind")
			return

		channel = self.bot.get_channel(int(target_channel))

		await utils.impersonate(self.bot, message.content, message.author, channel)
		await message.delete()

def setup(bot):
	bot.add_cog(Misc(bot))
	return True
