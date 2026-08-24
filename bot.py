import discord
from discord.ext import commands
import os
import random
import asyncio
import yt_dlp
from dotenv import load_dotenv
import static_ffmpeg
static_ffmpeg.add_paths()

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BLUE_GIF = os.path.join(BASE_DIR, "blue.gif")
ABHINAV_IMAGE = os.path.join(BASE_DIR, "images", "abhinav.png")

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN environment variable is not set!"
    )

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True
intents.voice_states = True 
#Update
bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# ==========================================
# BLUE TRIGGERS
# ==========================================

BLUE_TRIGGERS = [
    # Basic
    "blue",
    "bluu",
    "blu",
    "bluee",
    "blueee",

    # Song / lyrics
    "da ba dee",
    "dabadee",
    "da ba dee da ba die",
    "dabadie",
    "da ba di",
    "da ba dee da ba di",
    "blue da ba dee",
    "blue dabadee",
    "blue dabadi",
    "im blue",
    "i'm blue",
    "i am blue",
    "i'm blue dabadee",
    "i am blue dabadee",

    # Common references
    "blue song",
    "blue music",
    "blue guy",
    "blue dude",
    "blue man",
    "blue person",
    "blue boy",
    "blue character",
    "blue eiffel",
    "eiffel 65",
    "eiffel sixty five",
    "eiffel65",

    # Meme-style
    "who is blue",
    "why is he blue",
    "why is bro blue",
    "why is bro so blue",
    "bro is blue",
    "bro blue",
    "he is blue",
    "he's blue",
    "hes blue",
    "they're blue",
    "they are blue",
    "everyone is blue",
    "everything is blue",
    "blue everywhere",

    # Misspellings
    "da ba di da ba die",
    "dabadi dabadie",
    "daba dee",
    "dabadee",
    "dabadi",
    "im blu",
    "i'm blu",
    "iam blue",
    "i am blu",
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
    "abhinav",
    "abhi",
    "abhinav is here",
    "where is abhinav",
    "look at abhinav",
    "show abhinav",
    "cute abhinav",
    "cutie abhinav",
]

FFMPEG_OPTIONS = {
    "before_options": (
        "-reconnect 1 "
        "-reconnect_streamed 1 "
        "-reconnect_delay_max 5"
    ),
    "options": "-vn"
}

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    # REMOVED: cookiefile / cookiesfrombrowser 
    # ADDED: Forces yt-dlp to bypass broken web player handshakes
    "extractor_args": {
        "youtube": {
            "player_client": ["android", "ios"]
        }
    }
}

BLUE_URL = "https://www.youtube.com/watch?v=68ugkg9RePc"

def get_audio_url(url):
    with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)

        if "entries" in info:
            info = info["entries"][0]

        return info["url"]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    try:
        synced = await bot.tree.sync()
        print(f"Successfully synced {len(synced)} command(s).")

    except Exception as e:
        print(f"Failed to sync commands: {e}")

# ==========================================
# /bluegif
# ==========================================

@bot.tree.command(
    name="bluegif",
    description="Sends a clean Blue Da Ba Dee GIF"
)
async def bluegif(interaction: discord.Interaction):

    await interaction.response.defer()

    embed = discord.Embed(
        title="💙 Blue Da Ba Dee!",
        description=(
            f"Hey **{interaction.user.display_name}**, "
            "I'm Blue Da Ba DEE!"
        ),
        color=discord.Color.blue()
    )

    file = discord.File(
        BLUE_GIF,
        filename="blue.gif"
    )

    embed.set_image(
        url="attachment://blue.gif"
    )

    await interaction.followup.send(
        embed=embed,
        file=file
    )

@bot.event
async def on_presence_update(before, after):
    # Only trigger when someone goes from offline → online
    if before.status == discord.Status.offline and after.status != discord.Status.offline:

        # Ignore bots
        if after.bot:
            return

        # Find the general channel
        channel = discord.utils.get(
            after.guild.text_channels,
            name="general"
        )

        if channel is None:
            return

        # Create the message
        embed = discord.Embed(
            title="👋 HELLO!",
            description=(
                f"Welcome, **{after.display_name}**! 💙\n\n"
                "Have you listened to **I'm Blue (Da Ba Dee)**? 🎵🔵\n"
                "You absolutely need to hear it. 😭💙"
            ),
            color=discord.Color.blue()
        )

        # Load the GIF
        file = discord.File(
            BLUE_GIF,
            filename="blue.gif"
        )

        # Put GIF inside embed
        embed.set_image(
            url="attachment://blue.gif"
        )

        embed.set_footer(
            text="💙 Blue Da Ba Dee"
        )

        # Send message + GIF
        await channel.send(
            embed=embed,
            file=file
        )

@bot.tree.command(
    name="showabhinav",
    description="Shows the cutest Abhinav"
)
async def showabhinav(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🥹💙 THE CUTIE PIE HIMSELF",
        description=(
            "Everyone look‼️\n\n"
            "**Abhinav is such a cutie pie!** 🥹💙\n"
            "Absolutely adorable. 10/10 cuteness. 😭✨"
        ),
        color=discord.Color.blue()
    )

    file = discord.File(
        ABHINAV_IMAGE,
        filename="abhinav.png"
    )

    embed.set_image(
        url="attachment://abhinav.png"
    )

    await interaction.response.send_message(
        embed=embed,
        file=file
    )


# ==========================================
# MESSAGE LISTENER
# ==========================================
@bot.event
async def on_message(message):

    # Ignore bots
    if message.author.bot:
        return

    user_text = message.content
    username = message.author.display_name
    channel = getattr(
        message.channel,
        "name",
        "DM"
    )

    print(f"[{channel}] {username}: {user_text}")

    text = user_text.lower()

    # ==========================================
    # AUTOMATIC RESPONSES
    # ==========================================

    for trigger, responses in RESPONSES.items():

        if trigger in text:

            response = random.choice(responses)

            await message.channel.send(response)

            break

    # ==========================================
    # BLUE DETECTION
    # ==========================================

    if any(trigger in text for trigger in BLUE_TRIGGERS):

        embed = discord.Embed(
            title="💙 BLUE DA BA DEE!",
            description=(
                f"**Blue, {username}!** 🔵\n\n"
                "I'm Blue Da Ba Dee!"
            ),
            color=discord.Color.blue()
        )

        file = discord.File(
            BLUE_GIF,
            filename="blue.gif"
        )

        embed.set_image(
            url="attachment://blue.gif"
        )

        embed.set_footer(
            text="💙 Blue Da Ba Dee"
        )

        await message.channel.send(
            embed=embed,
            file=file
        )

    # ==========================================
    # ABHINAV DETECTION
    # ==========================================

    if any(trigger in text for trigger in ABHINAV_TRIGGERS):

        embed = discord.Embed(
            title="🥹💙 THE CUTIE PIE HIMSELF",
            description=(
                "Everyone look‼️\n\n"
                "**Abhinav is such a cutie pie!** 🥹💙\n"
                "Absolutely adorable. 10/10 cuteness. 😭✨"
            ),
            color=discord.Color.blue()
        )

        file = discord.File(
            ABHINAV_IMAGE,
            filename="abhinav.png"
        )

        embed.set_image(
            url="attachment://abhinav.png"
        )

        embed.set_footer(
            text="Abhinav appreciation department"
        )

        await message.channel.send(
            embed=embed,
            file=file
        )

    # ==========================================
    # KEEP COMMANDS WORKING
    # ==========================================

    await bot.process_commands(message)

@bot.tree.command(
    name="playblue", 
    description="Play Blue"
)
async def playblue(interaction: discord.Interaction):
    if interaction.user.voice is None:
        await interaction.response.send_message("🔵 Join a voice channel first!", ephemeral=True)
        return

    await interaction.response.defer()
    channel = interaction.user.voice.channel
    
    # Path to your local mp4 file
    BLUE_MP4 = os.path.join(BASE_DIR, "blue.mp4")
    
    if not os.path.exists(BLUE_MP4):
        await interaction.followup.send("❌ Error: `blue.mp4` file is missing from the server directory.")
        return

    try:
        voice_client = interaction.guild.voice_client
        if voice_client is None:
            voice_client = await channel.connect()
        elif voice_client.channel != channel:
            await voice_client.move_to(channel)

        if voice_client.is_playing():
            voice_client.stop()

        # FFmpeg reads the MP4 and streams the audio smoothly
        source = discord.FFmpegPCMAudio(
            BLUE_MP4, 
            executable="ffmpeg"
        )
        
        def after_playing(error):
            if error:
                print("Playback error:", error)

        voice_client.play(source, after=after_playing)
        await interaction.followup.send(f"💙 **BLUE DA BA DEE!** 🎵\nPlaying smoothly from media storage in **{channel.name}**!")
        
    except Exception as e:
        import traceback
        print("=== RAILWAY VOICE DEBUG START ===")
        traceback.print_exc()
        print("=== RAILWAY VOICE DEBUG END ===")
        
        error_message = str(e).strip() or "Internal voice initialization error. Check your Railway console logs."
        await interaction.followup.send(f"❌ Music failed:\n`{error_message}`")


@bot.tree.command(
    name="stop",
    description="Stop the current music"
)
async def stop(interaction: discord.Interaction):

    voice_client = interaction.guild.voice_client

    if voice_client is None:
        await interaction.response.send_message(
            "I'm not in a voice channel."
        )
        return

    if voice_client.is_playing():
        voice_client.stop()

    await interaction.response.send_message(
        "⏹️ **Blue has been stopped.**"
    )

@bot.tree.command(
    name="pause",
    description="Pause the music"
)
async def pause(interaction: discord.Interaction):

    voice_client = interaction.guild.voice_client

    if voice_client and voice_client.is_playing():

        voice_client.pause()

        await interaction.response.send_message(
            "⏸️ Music paused."
        )

    else:

        await interaction.response.send_message(
            "❌ Nothing is playing."
        )

@bot.tree.command(
    name="resume",
    description="Resume the music"
)
async def resume(interaction: discord.Interaction):

    voice_client = interaction.guild.voice_client

    if voice_client and voice_client.is_paused():

        voice_client.resume()

        await interaction.response.send_message(
            "▶️ Blue is back!"
        )

    else:

        await interaction.response.send_message(
            "❌ Nothing is paused."
        )

@bot.tree.command(
    name="leave",
    description="Make the bot leave the voice channel"
)
async def leave(interaction: discord.Interaction):

    voice_client = interaction.guild.voice_client

    if voice_client is None:
        await interaction.response.send_message(
            "I'm not in a voice channel."
        )
        return

    await voice_client.disconnect()

    await interaction.response.send_message(
        "👋 Left the voice channel."
    )

bot.run(TOKEN)
