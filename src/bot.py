from discord.ext import commands
import discord
from os import getenv
from dotenv import load_dotenv
import utils
import json
import asyncio
import praw

load_dotenv()

CONFIG_LOCATION = "config/config.json"
DEFAULT_CONFIG_LOCATION = "config/default_config.json"

# Check if config file exists
# If not, it will create a new config with default values
try:
	config_file = open(CONFIG_LOCATION)
except FileNotFoundError:
	config_file = open(CONFIG_LOCATION, "w+")
	default_config_file = open(DEFAULT_CONFIG_LOCATION)
	config_file.write(default_config_file.read())

config = json.load(config_file)

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
	# Set variables that will be accessible throughout
	bot.config = config
	bot.owner = bot.get_user(config['owner_id'])
	bot.reddit = praw.Reddit(user_agent=config['user_agent'])

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
	"cogs.fun",
	"cogs.meming",
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
