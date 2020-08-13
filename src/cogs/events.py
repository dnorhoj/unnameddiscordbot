import discord, utils
from discord.ext import commands

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		errors = {
			commands.errors.CheckFailure: "You don't have permission to do this!",
			commands.errors.MissingRequiredArgument: "Missing Argument!\nHelp command can help you with the usage.",
			commands.errors.BadArgument: "Invalid argument!",
			commands.errors.CommandNotFound: "Command not found!"
		}

		if not type(error) in errors:
			print("ERROR! {} ({})".format(type(error).__name__, ", ".join(error.args)))
			await ctx.send("Error! Unknown error!")
			return

		await ctx.send("Error! {}".format(errors[type(error)]))

def setup(bot):
	bot.add_cog(Events(bot))
	return True
