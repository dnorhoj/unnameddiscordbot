import discord
from discord.ext import commands
import itertools

class HelpCommand(commands.HelpCommand):
	#def __init__(self):
	#    super().__init__(command_attrs={
	#        'help': 'Shows help about the bot, a command, or a category'
	#    })

	def add_footer(self, ctx, embed):
		bot = ctx.bot
		return embed.set_footer(
			icon_url=bot.owner.avatar_url_as(format="png"),
			text=f"Bot made by {bot.owner.name}#{bot.owner.discriminator}"
		)

	async def on_help_command_error(self, ctx, error):
		bot = self.context.bot
		if isinstance(error, commands.CommandInvokeError):
			error_embed = discord.Embed(
				title="<:tcdisagree:623642279856570408> Error!",
				description=f"Unknown error!\nPlease message the bot owner if you've found an error.",
				color=discord.Color.red()
			)
			error_embed = self.add_footer(self.context, error_embed)
			await ctx.send(embed=error_embed)

	def get_command_signature(self, command):
		parent = command.full_parent_name
		if len(command.aliases) > 0:
			aliases = '|'.join(command.aliases)
			fmt = f'[{command.name}|{aliases}]'
			if parent:
				fmt = f'{parent} {fmt}'
			alias = fmt
		else:
			alias = command.name if not parent else f'{parent} {command.name}'
		return f'{self.context.prefix}{alias} {command.signature}'

	async def command_not_found(self, string):
		embed = discord.Embed(
			title="<:tcdisagree:623642279856570408> The command '{}' was not found!".format(string),
			color=discord.Color.red()
		)
		await self.context.send(embed=embed)

	async def send_error_message(self, error):
		# We need to overwrite send_error_message to be able to have an embed as command not found
		destination = self.get_destination()
		if not error is None:
			await destination.send(error)

	async def send_bot_help(self, mapping):
		def key(c):
			return c.cog_name or '\u200bNo Category'

		bot = self.context.bot
		entries = await self.filter_commands(bot.commands, sort=True, key=key)

		help_embed = discord.Embed(title="Command list", color=discord.Color.green())
		help_embed = self.add_footer(self.context, help_embed)

		for cog, commands in itertools.groupby(entries, key=key):
			commands = sorted(commands, key=lambda c: c.name)
			if len(commands) == 0:
				continue

			actual_cog = bot.get_cog(cog)
			description = actual_cog.description or "No description"

			contents = [description]
			contents.extend([f"`{self.get_command_signature(command).strip()}`" for command in commands])

			help_embed.add_field(name=cog, value="\n".join(contents), inline=False)

		await self.context.send(embed=help_embed)

	async def send_cog_help(self, cog):
		entries = await self.filter_commands(cog.get_commands(), sort=True)

		help_embed = discord.Embed(color=discord.Color.green())
		help_embed = self.add_footer(self.context, help_embed)

		description = cog.description or "No description"

		contents = [description]
		contents.extend([f"`{self.get_command_signature(entry).strip()}`" for entry in entries])
		help_embed.add_field(name=cog.qualified_name, value="\n".join(contents), inline=False)

		await self.context.send(embed=help_embed)

	async def send_command_help(self, command):
		# No pagination necessary for a single command.
		embed = discord.Embed(title="Usage", colour=discord.Colour.green())

		embed = self.add_footer(self.context, embed)

		description = []
		description.append(command.help or 'No description')
		description.append(f'`{self.get_command_signature(command)}`')

		embed.add_field(name=command.name, value="\n".join(description))
		await self.context.send(embed=embed)

	async def send_group_help(self, group):
		bot = self.context.bot
		subcommands = group.commands
		if len(subcommands) == 0:
			return await self.send_command_help(group)

		entries = await self.filter_commands(subcommands, sort=True)

		description = []
		description.append(group.help or 'No help found...')

		for entry in entries:
			description.append("`{}`".format(self.get_command_signature(entry)))

		help_embed = discord.Embed(title="Usage", color=discord.Color.green())
		help_embed = self.add_footer(self.context, help_embed)

		help_embed.add_field(name=group.name, value="\n".join(description))

		await self.context.send(embed=help_embed)


class Help(commands.Cog):
	"""Helps you discover commands and get usage help"""
	def __init__(self, bot):
		self._original_help_command = bot.help_command
		self.bot = bot
		bot.help_command = HelpCommand()
		bot.help_command.cog = self

	def cog_unload(self):
		self.bot.help_command = self._original_help_command

def setup(bot):
	bot.add_cog(Help(bot))
	return True
