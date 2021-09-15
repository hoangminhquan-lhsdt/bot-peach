import os
from discord.ext import commands, tasks
import aiohttp
from aiohttp import web
import asyncio
import base64
import requests
from .music import *

from .music import voice_states
class Server(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.music_player = self.bot.get_cog('Music')
		self.voice_state = None


	def get_voice_state(self, id) -> VoiceState:
		state = voice_states[id]
		# print(f'state: {state}')
		# if not state:
		# 	state = VoiceState(self.bot)
		# 	voice_states[self.id] = state
		return state


	async def webserver(self):
		self.web_app = web.Application()
		routes = web.RouteTableDef()

		@routes.get('/')
		async def home(request):
			return web.HTTPForbidden()


		@routes.get('/api/v1/info/get_user_info/{user_id}')
		async def get_user_info(request):
			r = requests.get('https://discord.com/api/users/'+request.match_info.get('user_id'), headers={'Authorization': 'Bot ODYzMzY0ODI4MzIzMTE5MTA0.YOl1Jw.lWtxDvhhvxuqw0LoMVxTEEP4aTI'})
			print(r.status_code)
			print(r.text)
			print(r.json())
			return web.json_response(r.json())


		@routes.get('/api/v1/info/get_guild_info/{guild_id}')
		async def get_guild_info(request):
			r = requests.get('https://discord.com/api/guilds/'+request.match_info.get('guild_id'), headers={'Authorization': 'Bot ODYzMzY0ODI4MzIzMTE5MTA0.YOl1Jw.lWtxDvhhvxuqw0LoMVxTEEP4aTI'})
			print(r.status_code)
			print(r.text)
			return web.json_response(r.json())


		@routes.get('/api/v1/info/get_guild_members/{guild_id}')
		async def get_guild_members(request):
			guild = self.bot.get_guild(int(request.match_info.get('guild_id')))
			members = [member.id for member in guild.members]
			res = web.json_response({'ids': members})
			return res


		@routes.get('/api/v1/info/user_in_guild/{guild_id}/{user_id}')
		async def user_in_guild(request):
			guild = self.bot.get_guild(int(request.match_info.get('guild_id')))
			members = [member.id for member in guild.members]
			res = web.json_response({'response': int(request.match_info.get('user_id')) in members})
			return res


		@routes.get('/api/v1/music/get_playlist')
		async def get_playlist(request):
			body = await request.json()
			id = body['guild_id']
			# id = 791003246973288478
			self.voice_state = self.get_voice_state(id)
			res = dict(zip(list(range(len(self.voice_state.songs))),
				[{
					'name': song.source.title,
					'duration': song.source.duration,
					'requester': song.requester.name + '#' + song.requester.discriminator
				}
				for i, song in enumerate(self.voice_state.songs)]))
			return web.json_response(res)

		test_res = [
			{
				'name': "Coldplay - Ink (Official Fans' Cut Video)",
				'duration': 228,
				'requester': "Hạc"
			},
			{
				'name': "Aimer - Kataomoi",
				'duration': 222,
				'requester': "Hạc"
			},
			{
				'name': "Imagine Dragons - Wrecked (Official Music Video)",
				'duration': 277,
				'requester': "Hạc"
			},
			{
				'name': "Post Malone, Swae Lee - Sunflower (Spider-Man: Into the Spider-Verse)",
				'duration': 162,
				'requester': "Hạc"
			},
			{
				'name': "Radiohead - Creep",
				'duration': 237,
				'requester': "Hạc"
			},
			{
				'name': "The Fratellis - Whistle For The Choir",
				'duration': 216,
				'requester': "Hạc"
			},
			{
				'name': "Edward Sharpe & The Magnetic Zeros - Home (Official Video)",
				'duration': 307,
				'requester': "Hạc"
			},
		]
		@routes.get('/api/v1/music/get_playlist_test')
		async def get_playlist_test(request):
			return web.json_response(test_res)
			# return web.Response(body=test_res, status=200)


		@routes.post('/api/v1/music/remove_song_from_playlist_test')
		async def remove_song_from_playlist_test(request):
			body = await request.json()
			indexes = body['index']
			res = []
			for i, song in enumerate(test_res):
				if i+1 not in indexes:
					res.append(song)
			return web.json_response(res, status=200)


		self.web_app.add_routes(routes)
		self.runner = web.AppRunner(self.web_app)
		await self.runner.setup()
		self.site = web.TCPSite(self.runner, '0.0.0.0', os.environ['PORT'])
		await self.bot.wait_until_ready()
		await self.site.start()


	def __unload(self):
		asyncio.ensure_future(self.site.stop())