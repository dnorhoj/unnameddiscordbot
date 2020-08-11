from discord.ext import commands
import discord
from os import getenv
from dotenv import load_dotenv
import utils
import json
import asyncio

load_dotenv()
config = json.load(open("config/config.json"))

async def get_command_prefix(bot, msg):
	prefixes = []
	prefixes.extend(config['prefixes'])
	prefixes.append(f'{bot.user.mention} ')

	if msg.channel.type.name == discord.ChannelType.private.name:
		prefixes.append("")

	return prefixes

bot = commands.Bot(command_prefix=get_command_prefix)
#bot.remove_command("help")

@bot.event
async def on_ready():
	bot.owner = bot.get_user(config['owner_id'])
	print("""---Info---
	Successfully started.
	Running on user: {}
	---Info---""".replace("\t", "").format(bot.user))
	await bot.change_presence(activity=discord.Game(config["status_game"]))

# Define cogs to load
cogs = [
	"cogs.help",
	"cogs.hashing",
	"cogs.events",
	"cogs.misc",
	"cogs.fun"
]

# Load cogs
if __name__ == "__main__":
	lst = []
	for cog in cogs:
		try:
			bot.load_extension(cog)
			lst.append(cog.replace("cogs.",""))
		except Exception as e:
			exc = "{}: {}".format(type(e).__name__, str(e))
			print("Failed to load {}\n{}".format(cog, exc))

	out = ", ".join(lst)[::-1].replace(",", " and"[::-1], 1)[::-1]
	print("Loaded: {}".format(out))

# Start bot
bot.run(getenv("DISCORD_TOKEN"))
