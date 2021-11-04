#region ------------------------------------------------------ SETUP -------------------------------------------------

from os import system
import discord
from discord.ext import commands
import os
import platform
import json

if not os.path.isfile('config.json'):
	def_config = {
		'token': '',
		'intents': {'messages': False, 'members': False, 'guilds': False},
		'prefix': '-',
		'admins': []
	}
	with open('config.json', 'w') as outfile:
		json.dump(def_config, outfile, indent=4)

with open('config.json') as json_file:
    config = json.load(json_file)

intents = discord.Intents.default()
intents.messages = config['intents']['messages']
intents.members = config['intents']['members']
intents.guilds = config['intents']['guilds']

prefix = config['prefix']

activity = discord.Game(name=f"{prefix}help")
bot = commands.Bot(command_prefix = prefix, intents=intents, activity=activity, status=discord.Status.online, case_insensitive=True)
bot.remove_command('help')

bot.token = config['token']
bot.admins = config['admins']


#endregion

#region ------------------------------------------------- CUSTOM FUNCTIONS -------------------------------------------

def clear():
	if platform.system() == 'Windows':
		system('cls')
	else:
		# system('clear')
		pass

def admin(ctx):
	return True if ctx.author.id in bot.admins else False
#endregion

#region ----------------------------------------------------- EVENTS -------------------------------------------------

@bot.event																	# Startup
async def on_ready():
	clear()
	print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_member_join(member):
	print('"' + member.name + '" joined')

#endregion

#region ----------------------------------------------------- COMMANDS -------------------------------------------------

@bot.command()
async def ping(ctx):
	await ctx.send('Pong!')

@bot.command()
async def reload(ctx):
	if admin(ctx):
		await ctx.send('Reloading...')
		if platform.system() == 'Windows' and os.path.isfile('run.bat'):
			os.system('run.bat')
			quit()
		elif os.path.isfile('run.sh'):
			os.system('./run.sh')
			quit()
		else:
			await ctx.send('An error has occured')
	else:
		await ctx.send('You do not have permission to do that!')

@bot.command()
async def help(ctx):
	embed = discord.Embed ( # Message
		title='Help Commands',
		description=f'Listing commands...',
		colour=discord.Colour.blue()
	)
	await ctx.send(embed=embed)

#endregion

#region ----------------------------------------------------- COGS -------------------------------------------------
blacklist = ['template.py']

for filename in os.listdir('./cogs'):
	if filename.endswith('.py') and filename not in blacklist:
		bot.load_extension(f'cogs.{filename[:-3]}')

#endregion


clear()
print('Booting Up...')

bot.run(bot.token)