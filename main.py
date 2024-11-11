import discord
import os
import dotenv
import asyncio
import sys
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
bot = discord.Bot()
target_text_channel_id = None
target_voice_channel_id = None
# Define the check_time function
async def check_time():
    await bot.wait_until_ready()  # Wait until the bot is ready
    global target_text_channel_id  # Get the text channel
    global target_voice_channel_id  # Get the voice channel
    while not bot.is_closed() :  # While the bot is running

        now = datetime.now()  # Get the current time

        # Check if the current time is divisble by 10
        if target_text_channel_id is not None and now.second % 10 == 0:
            channel = bot.get_channel(target_text_channel_id)
            if channel is not None:
                await channel.send(f"Bing bong! {now.strftime('%H:%M:%S')}")
        if target_voice_channel_id is not None and now.second % 30 == 0:
            channel = bot.get_channel(target_voice_channel_id)
            
            if channel and isinstance(channel, discord.VoiceChannel):
                # Check if the bot is already connected to the voice channel
                voice_client = discord.utils.get(bot.voice_clients, guild=channel.guild)

                # If not connected, connect to the channel
                if voice_client is None:
                    voice_client = await channel.connect()
                    print(f"Joined channel: {channel.name}")
                
                # Play the audio file if the bot is connected and not playing anything
                if voice_client.is_playing():
                    print("Bot is already playing audio.")
                else:
                    try:
                        source = discord.FFmpegPCMAudio("ack.mp3")  # Replace with the correct path
                        source = discord.PCMVolumeTransformer(source, volume = 1.0)
                        print("Playing audio...")
                        try:
                            voice_client.play(source, after=lambda e: print('done', e))
                        except Exception as e:
                            print(f"Error playing audio: {e}")
                    except Exception as e:
                        print(f"Error playing audio: {e}")
                try:
                    while voice_client.is_playing():
                        await asyncio.sleep(1)
                    await voice_client.disconnect()
                    print(f"Disconnected from voice channel: {channel.name}")
                except Exception as e:
                    print(f"Error disconnecting from voice channel: {e}")
        await asyncio.sleep(1)  # Wait for 1 second before checking again

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    bot.loop.create_task(check_time())  # Create the task

@bot.slash_command(name="set_text_channel", description="Set the text channel to send the time")
async def set_text_channel(ctx: discord.ApplicationContext, channel: discord.TextChannel):
    global target_text_channel_id
    target_text_channel_id = ctx.channel.id
    await ctx.respond(f"Text channel set to this channel: {channel.name}")

@bot.slash_command(name="set_voice_channel", description="Set the voice channel to send the time")
async def set_voice_channel(ctx: discord.ApplicationContext, channel: discord.VoiceChannel):
    global target_voice_channel_id
    target_voice_channel_id = channel.id
    await ctx.respond(f"Voice channel set to this channel: {channel.name}")

@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")

@bot.slash_command(name="time", description="Get the current time")
async def time(ctx: discord.ApplicationContext):
    await ctx.respond(f"The current time is {datetime.now().strftime('%H:%M:%S')}")

@bot.slash_command(name="ping", description="Check the bot's latency")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f"Pong! {bot.latency * 1000}ms")

@bot.slash_command(name="restart", description="Restarts the bot")
async def restart(ctx):
    """This command restarts the bot."""
    await ctx.respond("Bot is restarting...")  # Respond to the user
    await bot.close()  # Disconnect the bot
    os.execv(sys.executable, ['python'] + sys.argv)  # Restart the bot

bot.run(os.getenv('DISCORD_TOKEN'))




