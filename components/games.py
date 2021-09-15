import random
import discord
from discord.ext import commands


class Games(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name='dice', aliases=['roll'])
	async def _dice(self, ctx: commands.Context):
		'''Roll a dice'''
		await ctx.message.add_reaction('✅')
		return await ctx.send(f':game_die: {random.randint(1, 6)}')

	@commands.command(name='random', aliases=['rnd'])
	async def _random(self, ctx: commands.Context, *, range: str=None):
		'''Get a random number'''
		await ctx.message.add_reaction('✅')
		if range is None:
			return await ctx.send(random.randint(0, 1000000000))
		else:
			r = range.split(' ')
			if len(r) == 1:
				return await ctx.send(f':ballot_box_with_check: {random.randint(0, int(r[0]))}')
			elif len(r) == 2:
				return await ctx.send(f':ballot_box_with_check: {random.randint(int(r[0], int(r[1])))}')
			else:
				return await ctx.send(f':ballot_box_with_check: {random.choice(r)}')