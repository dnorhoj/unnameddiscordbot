import discord, random, asyncio
from discord.ext import commands

class Fun(commands.Cog):
	def __init__(self, bot:discord.Client):
		self.bot = bot

	@commands.command()
	async def minesweeper(self, ctx:discord.ext.commands.Context, gridsize:int=None, bombs:int=None):
		if bombs is None: # Not enough arguments
			# Generate embed to send
			embed = discord.Embed(title=":exclamation: Not enough arguments.", description="Usage: `{0.prefix}{0.invoked_with} [size] [bombs]`".format(ctx), colour=0xff0000)
			await ctx.send(embed=embed)
			return

		if bombs > gridsize**2:
			embed = discord.Embed(title=":exclamation: Too many bombs.", description="Bomb amount is more than total grid.", colour=0xff0000)
			await ctx.send(embed=embed)
			return

		# Generate coordinate system
		coordinates = {}
		for x in range(gridsize):
			for y in range(gridsize):
				coordinates[str(x)+str(y)] = "" # Define location existence

		for randomindex in random.sample(list(coordinates), bombs): # Get random locations for bombs
			coordinates[randomindex] = "x" # Make the selected index a bomb

		for c in coordinates:
			# If the current coordinate is a bomb, skip
			if coordinates[c] == "x":
				continue

			x, y = list(c) # Get current iteration's coordinates
			bcount = 0 # Count of bombs in neighborhood

			# Iterate to check if any bomb in neighborhood
			for xo in range(-1,2):
				for yo in range(-1,2):
					nx, ny = int(x)+xo, int(y)+yo

					if nx < 0 or nx > gridsize-1 or ny < 0 or ny > gridsize-1:
						continue

					if coordinates[str(nx)+str(ny)] == "x":
						bcount+=1
			coordinates[c] = bcount

		map = { 0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", "x": "bomb" }

		res = ""
		i = 0
		for c in coordinates:
			if i == gridsize:
				res+='\n'
				i=0
			res += "||:{}:||".format(map[coordinates[c]])
			i+=1

		await ctx.send(res)

def setup(bot):
	bot.add_cog(Fun(bot))
	return True
