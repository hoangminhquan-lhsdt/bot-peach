import os
import logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

import discord
from discord.ext import commands

from components.admin import Admin
from components.games import Games
from components.math import Math
from components.music import Music
from components.server import Server


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)


@bot.event
async def on_ready():
	print(f'\n{bot.user} has connected to Discord!')
	print('-'*15)


admin_commands_dict = {
	'`shutdown`': {'aliases': '`\u200b`', 'desc':'`Shutdown the bot`'},
	'`restart`': {'aliases': '`\u200b`', 'desc':'`Restart the bot`'},
}

music_commands_dict = {
	'`summon`': {'aliases': '`\u200b`', 'desc': '`Join the voice channel`'},
	'`leave`' : {'aliases': '`disconnect`', 'desc': '`Leave the voice channel`'},
	'`volume <number>`': {'aliases': '`\u200b`', 'desc': '`Set the playback volume`'},
	'`play <name/link>`': {'aliases': '`p`', 'desc': '`Play a song`'},
	'`pause`': {'aliases': '`\u200b`', 'desc': '`Pause playback`'},
	'`resume`': {'aliases': '`\u200b`', 'desc': '`Resume playback`'},
	'`nowplaying`' : {'aliases': '`current`, `playing`', 'desc': '`Print current song`'},
	'`queue`': {'aliases': '`q`, `playlist`', 'desc': '`Print song queue`'},
	'`stop`' : {'aliases': '`\u200b`', 'desc': '`Stop playback`'},
	'`skip`' : {'aliases': '`\u200b`', 'desc': '`Skip a song`'},
	'`shuffle`' : {'aliases': '`\u200b`', 'desc': '`Shuffle queue`'},
	'`loop`' : {'aliases': '`\u200b`', 'desc': '`Loop current song`'},
	'`remove <index(es)>`': {'aliases': '`\u200b`', 'desc': '`Remove song(s) from list`'},
	'`save_queue <name>`': {'aliases': '`save_playlist`', 'desc': '`Save current queue`'},
	'`load_queue <name>`': {'aliases': '`load_playlist`', 'desc': '`Load saved queue`'},
	'`upload_queue <file>`': {'aliases': '`upload_playlist`', 'desc': '`Upload a queue`'},
	# '`list_queues`': {'aliases': '`list_playlists`', 'desc': '`List available queues`'},
	# '`delete_queue <name>`': {'aliases': '`delete_playlist`', 'desc': '`Delete saved queue`'},
	# '`download_queue <name>`': {'aliases': '`download_playlist`', 'desc': '`Download saved queue`'},
	# '`download_all_queues`': {'aliases': '`download_all_playlists`', 'desc': '`Download all saved queues`'},
}

maths_commands_dict = {
	'`latex <expression>`': {'aliases': '`\u200b`', 'desc': '`Render a LaTeX expression`'},
}

games_commands_dict = {
	'`dice`': {'aliases': '`roll`', 'desc': '`Roll a dice`'},
	'`random`': {'aliases': '`rnd`', 'desc': '`Random number`'}
}

@bot.command()
async def help(ctx: commands.Context):
	embed = discord.Embed(color=discord.Color.blurple(), title='Commands list')

	# admin_cmds = list(admin_commands_dict.keys())
	# admin_alis = [cmd['aliases'] for cmd in admin_commands_dict.values()]
	# admin_dscs = [cmd['desc'] for cmd in admin_commands_dict.values()]

	# embed.add_field(name='Admin commands', value='\n'.join(admin_cmds), inline=True)
	# embed.add_field(name='Aliases', value='\n'.join(admin_alis), inline=True)
	# embed.add_field(name='Description', value='\n'.join(admin_dscs), inline=True)

	music_cmds = list(music_commands_dict.keys())
	music_alis = [cmd['aliases'] for cmd in music_commands_dict.values()]
	music_dscs = [cmd['desc'] for cmd in music_commands_dict.values()]

	embed.add_field(name='Music commands', value='\n'.join(music_cmds), inline=True)
	embed.add_field(name='Aliases', value='\n'.join(music_alis), inline=True)
	embed.add_field(name='Description', value='\n'.join(music_dscs), inline=True)

	maths_cmds = list(maths_commands_dict.keys())
	maths_alis = [cmd['aliases'] for cmd in maths_commands_dict.values()]
	maths_dscs = [cmd['desc'] for cmd in maths_commands_dict.values()]

	embed.add_field(name='Maths commands', value='\n'.join(maths_cmds), inline=True)
	embed.add_field(name='\u200b', value='\n'.join(maths_alis), inline=True)
	embed.add_field(name='\u200b', value='\n'.join(maths_dscs), inline=True)

	games_cmds = list(games_commands_dict.keys())
	games_alis = [cmd['aliases'] for cmd in games_commands_dict.values()]
	games_dscs = [cmd['desc'] for cmd in games_commands_dict.values()]

	embed.add_field(name='Games commands', value='\n'.join(games_cmds), inline=True)
	embed.add_field(name='\u200b', value='\n'.join(games_alis), inline=True)
	embed.add_field(name='\u200b', value='\n'.join(games_dscs), inline=True)

	embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
	await ctx.send(embed=embed)


bot.add_cog(Admin(bot))
bot.add_cog(Games(bot))
bot.add_cog(Math(bot))
bot.add_cog(Music(bot))
server = Server(bot)
bot.add_cog(server)
bot.loop.create_task(server.webserver())
bot.run('bot-token')