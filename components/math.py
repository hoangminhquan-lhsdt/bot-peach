import os
import discord
from discord.ext import commands
from urllib import request, parse
import json
import base64


class Math(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command()
	async def latex(self, ctx: commands.Context, *, expr):
		async def generate_latex(expr):
			url = 'https://latex.oncodecogs.com/png.json?\\huge\\color{white}{' + parse.quote(expr) + '}'
			response = request.urlopen(url).read()
			return response

		async with ctx.typing():
			json_response = await generate_latex(expr)
			json_data = json.loads(json_response.decode('utf-8').replace("'", '"'))
			img = base64.b64decode(json_data['latex']['base64'])
			with open('latex.png', 'wb') as f:
				f.write(img)
		with open('latex.png', 'rb') as f:
			img = discord.File(f)
			await ctx.send(file=img)
