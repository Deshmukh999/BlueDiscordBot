import discord
from discord.ext import commands
import os
import random
import asyncio
from dotenv import load_dotenv

# INITIALIZE BINARIES: Automatically downloads/locates FFmpeg inside the virtual environment
import static_ffmpeg
static_ffmpeg.add_paths()

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLUE_GIF = os.path.join(BASE_DIR, "blue.gif")
ABHINAV_IMAGE = os.path.join(BASE_DIR, "images", "abhinav.png")
BLUE_MP4 = os.path.join(BASE_DIR, "blue.mp4")

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is not set!")

# INTENTS INITIALIZATION: voice_states is required for VC tracking
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True
intents.voice_states = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================================
# TRIGGER DATA POOLS
# ==========================================
BLUE_TRIGGERS = [
    "blue", "bluu", "blu", "bluee", "blueee",
    "da ba dee", "dabadee", "da ba dee da ba die", "dabadie", "da ba di", "da ba dee da ba di", 
    "blue da ba dee", "blue dabadee", "blue dabadi", "im blue", "i'm blue", "i am blue", 
    "i'm blue dabadee", "i am blue dabadee", "blue song", "blue music", "blue guy", 
    "blue dude", "blue man", "blue person", "blue boy", "blue character", "blue eiffel", 
    "eiffel 65", "eiffel sixty five", "eiffel65", "who is blue", "why is he blue", 
    "why is bro blue", "why is bro so blue", "bro is blue", "bro blue", "he is blue", 
    "he's blue", "hes blue", "they're blue", "they are blue", "everyone is blue", 
    "everything is blue", "blue everywhere", "da ba di da ba die", "dabadi dabadie", 
    "daba dee", "im blu", "i'm blu", "iam blue", "i am blu"
]

RESPONSES = {
    "good morning": [
        "Good morning! 💙", 
        "Morning! Have you listened to Blue yet? 🔵", 
        "Good morning! ☀️💙 The Blue Department welcomes you.", 
        "Morning! 🎵 Don't forget your daily dose of Blue!"
    ],
    "good night": [
        "Good night! 💙", 
        "Sweet dreams, Blue enjoyer. 🌙🔵", 
        "Good night! Don't let the Blue Da Ba Dee dreams get you. 💙", 
        "Sleep well! 🎵💙"
    ],
    "hello": [
        "Hello! 👋💙", 
        "BLUE welcomes you. 🔵", 
        "Hello there! 💙 Have you listened to Blue today?", 
        "Greetings, fellow Blue enjoyer. 😎🔵"
    ]
}

ABHINAV_TRIGGERS = [
    "abhinav", "abhi", "abhinav is here", "where is abhinav", 
    "look at abhinav", "show abhinav", "cute abhinav", "cutie abhinav"
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"Successfully synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# ==========================================
# SLASH COMMAND: /bluegif
# ==========================================
@bot.tree.command(name="bluegif", description="Sends a clean Blue Da Ba Dee GIF")
async def bluegif(interaction: discord.Interaction):
    await interaction.response.defer()
    if not os.path.exists(BLUE_GIF):
        await interaction.followup.send("❌ Error: `blue.gif` file missing from host directory.")
        return
    
    embed = discord.Embed(
        title="💙 Blue Da Ba Dee!",
        description=f"Hey **{interaction.user.display_name}**, I'm Blue Da Ba DEE!",
        color=discord.Color.blue()
    )
    file = discord.File(BLUE_GIF, filename="blue.gif")
    embed.set_image(url="attachment://blue.gif")
    await interaction.followup.send(embed=embed, file=file)

# ==========================================
# VOICE PRESENCE WELCOME DETECTOR
# ==========================================
@bot.event
async def on_presence_update(before, after):
    if after.bot:
        return
        
    if before.status == discord.Status.offline and after.status != discord.Status.offline:
        channel = discord.utils.get(after.guild.text_channels, name="general")
        if channel is None or not os.path.exists(BLUE_GIF):
            return

        embed = discord.Embed(
            title="👋 HELLO!",
            description=(
                f"Welcome, **{after.display_name}**! 💙\n\n"
                "Have you listened to **I'm Blue (Da Ba Dee)**? 🎵🔵\n"
                "You absolutely need to hear it. 😭💙"
            ),
            color=discord.Color.blue()
        )
        file = discord.File(BLUE_GIF, filename="blue.gif")
        embed.set_image(url="attachment://blue.gif")
        embed.set_footer(text="💙 Blue Da Ba Dee")
        await channel.send(embed=embed, file=file)

# ==========================================
# SLASH COMMAND: /showabhinav
# ==========================================
@bot.tree.command(name="showabhinav", description="Shows the cutest Abhinav")
async def showabhinav(interaction: discord.Interaction):
    if not os.path.exists(ABHINAV_IMAGE):
        await interaction.response.send_message("❌ Error: `abhinav.png` missing from images subdirectory.", ephemeral=True)
        return

    embed = discord.Embed(
        title="🥹💙 THE CUTIE PIE HIMSELF",
        description=(
            "Everyone look‼️\n\n"
            "**Abhinav is such a cutie pie!** 🥹💙\n"
            "Absolutely adorable. 10/10 cuteness. 😭✨"
        ),
        color=discord.Color.blue()
    )
    file = discord.File(ABHINAV_IMAGE, filename="abhinav.png")
    embed.set_image(url="attachment://abhinav.png")
    await interaction.response.send_message(embed=embed, file=file)

# ==========================================
# CHAT LOGIC AND AUTO-RESPONSES
# ==========================================
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_text = message.content
    username = message.author.display_name
    text = user_text.lower()
    
    responded = False
    for trigger, responses in RESPONSES.items():
        if trigger in text:
            response = random.choice(responses)
            await message.channel.send(response)
            responded = True
            break

    if not responded:
        if any(trigger in text for trigger in BLUE_TRIGGERS):
            if os.path.exists(BLUE_GIF):
                embed = discord.Embed(
                    title="💙 BLUE DA BA DEE!",
                    description=f"**Blue, {username}!** 🔵\n\nI'm Blue Da Ba Dee!",
                    color=discord.Color.blue()
                )
                file = discord.File(BLUE_GIF, filename="blue.gif")
                embed.set_image(url="attachment://blue.gif")
                embed.set_footer(text="💙 Blue Da Ba Dee")
                await message.channel.send(embed=embed, file=file)
                
        elif any(trigger in text for trigger in ABHINAV_TRIGGERS):
            if os.path.exists(ABHINAV_IMAGE):
                embed = discord.Embed(
                    title="🥹💙 THE CUTIE PIE HIMSELF",
                    description=(
                        "Everyone look‼️\n\n"
                        "**Abhinav is such a cutie pie!** 🥹💙\n"
                        "Absolutely adorable. 10/10 cuteness. 😭✨"
                    ),
                    color=discord.Color.blue()
                )
                file = discord.File(ABHINAV_IMAGE, filename="abhinav.png")
                embed.set_image(url="attachment://abhinav.png")
                embed.set_footer(text="Abhinav appreciation department")
                await message.channel.send(embed=embed, file=file)

    await bot.process_commands(message)

# ==========================================
# REINFORCED SLASH COMMAND: /playblue
# ==========================================
@bot.tree.command(name="playblue", description="Play Blue instantly in your voice channel")
async def playblue(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("🔵 Join a voice channel first!", ephemeral=True)
        return

    await interaction.response.defer()
    channel = interaction.user.voice.channel

    if not os.path.exists(BLUE_MP4):
        await interaction.followup.send("❌ Error: `blue.mp4` asset file was not found inside the root server directory.")
        return

    try:
        voice_client = interaction.guild.voice_client
        if voice_client is None:
            voice_client = await channel.connect()
        elif voice_client.channel != channel:
            await voice_client.move_to(channel)

        if voice_client.is_playing():
            voice_client.stop()

        # FIX: static-ffmpeg returns paths within an array/list. 
        # We index [0] to extract the clean, single-string absolute path to avoid crashing discord.py.
        raw_paths = static_ffmpeg.run.get_command_paths("ffmpeg")
        ffmpeg_bin_path = raw_paths[0] if isinstance(raw_paths, list) else raw_paths

        source = discord.FFmpegPCMAudio(
            BLUE_MP4, 
            executable=ffmpeg_bin_path
        )
        
        def after_playing(error):
            if error:
                print("Playback error encountered:", error)

        voice_client.play(source, after=after_playing)
        await interaction.followup.send(f"💙 **BLUE DA BA DEE!** 🎵\nPlaying smoothly in **{channel.name}**!")
    except Exception as e:
        import traceback
        print("=== RAILWAY VOICE DEBUG START ===")
        traceback.print_exc()
        print("=== RAILWAY VOICE DEBUG END ===")
        
        error_message = str(e).strip() or "Internal runtime connection error. Inspect the Railway Application Dashboard for details."
        await interaction.followup.send(f"❌ Music failed:\n`{error_message}`")

# ==========================================
# VC PLUG CONTROLS
# ==========================================
@bot.tree.command(name="stop", description="Stop the current music")
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client is None:
        await interaction.response.send_message("I'm not in a voice channel.", ephemeral=True)
        return
    if voice_client.is_playing():
        voice_client.stop()
    await interaction.response.send_message("⏹️ **Blue has been stopped.**")

@bot.tree.command(name="pause", description="Pause the music")
async def pause(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await interaction.response.send_message("⏸️ Music paused.")
    else:
        await interaction.response.send_message("❌ Nothing is playing.", ephemeral=True)

@bot.tree.command(name="resume", description="Resume the music")
async def resume(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await interaction.response.send_message("▶️ Blue is back!")
    else:
        await interaction.response.send_message("❌ Nothing is paused.", ephemeral=True)

@bot.tree.command(name="leave", description="Make the bot leave the voice channel")
async def leave(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client is None:
        await interaction.response.send_message("I'm not in a voice channel.", ephemeral=True)
        return
    await voice_client.disconnect()
    await interaction.response.send_message("👋 Left the voice channel.")

bot.run(TOKEN)
