import discord
from discord.ext import commands
from random import randint
import praw

class Meming(commands.Cog):
	"""Pulls memes from different subreddits"""
	def __init__(self, bot):
		self.bot = bot

	async def _subreddit_image_grabber(self, ctx, subreddit):
		"""Gets a random meme from `subreddit`"""
		loading_embed = discord.Embed(
			title=":arrows_counterclockwise: Loading...",
			description=f"Requested by @{ctx.author}"
		)

		tmp_message = await ctx.send(embed=loading_embed)
		subreddit = self.bot.reddit.subreddit(subreddit)

		# Get submissions for the selected subreddit
		submissions = list(subreddit.hot(limit=100))

		# Don't select stickied posts
		submission_num = randint(0, 100)
		while submissions[submission_num].stickied:
			submission_num = randint(0,99)
		submission = submissions[submission_num]

		try:
			if submission.over_18:
				error_embed = discord.Embed(
					title="<:tcdisagree:623642279856570408> Error!",
					description="Post is 18+!"
				)

				await tmp_message.edit(embed=error_embed)
				return

			elif submission.post_hint != "image":
				error_embed = discord.Embed(
					title="<:tcdisagree:623642279856570408> Error!",
					description="Post is not an image post."
				)

				await tmp_message.edit(embed=error_embed)
				return
		except AttributeError:
			error_embed = discord.Embed(
				title="<:tcdisagree:623642279856570408> Error!",
				description="Post is not an image post."
			)

			await tmp_message.edit(embed=error_embed)
			return

		# Create embed with title that links to post
		embed = discord.Embed(
			title=submission.title,
			url=f"https://reddit.com{submission.permalink}",
			color=discord.Color.green()
		)

		# Set author to the author of the post
		embed.set_author(
			name=f"u/{submission.author.name}",
			icon_url=submission.author.icon_img,
			url=f"https://reddit.com/user/{submission.author.name}"
		)

		# Set image url
		embed.set_image(url=submission.url)

		# Set footer to source and upvote counts
		embed.set_footer(
			text=f"Source: r/{subreddit} | {submission.ups} upvotes"
		)

		await tmp_message.edit(embed=embed)
		await tmp_message.add_reaction(emoji="👍")
		await tmp_message.add_reaction(emoji="👎")

	@commands.command()
	async def meme(self, ctx):
		"""Gets a meme from r/memes"""
		await self._subreddit_image_grabber(ctx, "memes")

	@commands.command()
	async def dankmeme(self, ctx):
		"""Gets a meme from r/dankmemes"""
		await self._subreddit_image_grabber(ctx, "dankmemes")

	@commands.command(aliases=["custom", "subreddit"])
	async def custom_meme(self, ctx, subreddit: str):
		"""Gets a meme from specified subreddit"""
		await self._subreddit_image_grabber(ctx, subreddit)

def setup(bot):
	bot.add_cog(Meming(bot))
	return True