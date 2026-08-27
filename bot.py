import discord
from discord.ext import commands
import os
import re
import random
import asyncio
import unicodedata
from difflib import SequenceMatcher
import yt_dlp
from dotenv import load_dotenv

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

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


def normalize_text(text: str) -> str:
    """Lowercase, strip accents, remove punctuation, collapse repeated chars."""
    text = text.lower().strip()

    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))

    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)

    text = re.sub(r"(.)\1{2,}", r"\1\1", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


def fuzzy_match(word: str, keyword: str, threshold: float = 0.82) -> bool:
    """True if word is similar enough to keyword to count as a match."""
    if not word or not keyword:
        return False
    return SequenceMatcher(None, word, keyword).ratio() >= threshold


def contains_fuzzy_keyword(text: str, keywords: list, threshold: float = 0.82) -> bool:
    """
    Checks normalized text for:
      - fuzzy single-word matches against keywords longer than 3 chars
      - EXACT token matches for short keywords (<=3 chars) to avoid noise
      - substring / sliding-window fuzzy matches for multi-word phrases
    """
    norm = normalize_text(text)
    if not norm:
        return False

    tokens = norm.split()
    token_set = set(tokens)

    for raw_keyword in keywords:
        keyword = normalize_text(raw_keyword)
        if not keyword:
            continue

        if " " in keyword:
            if keyword in norm:
                return True

            kw_tokens = keyword.split()
            n = len(kw_tokens)
            if len(tokens) >= n:
                for i in range(len(tokens) - n + 1):
                    window = " ".join(tokens[i:i + n])
                    if fuzzy_match(window, keyword, threshold=0.85):
                        return True

        else:
            if len(keyword) <= 3:
                if keyword in token_set:
                    return True
            else:
                for token in tokens:
                    if fuzzy_match(token, keyword, threshold=threshold):
                        return True

    return False


BLUE_KEYWORDS = [
    "blue", "im blue", "i am blue", "da ba dee", "da ba di",
    "da ba dee da ba di", "eiffel 65", "eiffel sixty five",
    "blue song", "blue music", "blue guy", "blue dude", "blue man",
    "blue person", "blue boy", "blue character", "who is blue",
    "why is he blue", "why is bro blue", "bro is blue", "he is blue",
    "they are blue", "everyone is blue", "everything is blue",
    "blue everywhere",

    "neela", "nila", "neela rang", "main neela hoon", "wo neela hai",

    "azul", "soy azul", "cancion azul", "hombre azul",

    "bleu", "je suis bleu", "chanson bleue",

    "blau", "ich bin blau", "blaues lied",

    "azul cancao", "sou azul",

    "blu", "sono blu",
]

ABHINAV_KEYWORDS = [
    "abhinav", "abhi", "where is abhinav", "show abhinav",
    "cute abhinav", "cutie abhinav", "look at abhinav",
    "abhinav is here",
]

GREETING_KEYWORDS = {
    "good morning": [
        "good morning", "gm", "morning",
        "suprabhat", "shubh prabhat",      # Hindi
        "buenos dias",                      # Spanish
        "bonjour",                          # French
        "guten morgen",                     # German
        "bom dia",                          # Portuguese
        "buongiorno",                       # Italian
    ],
    "good night": [
        "good night", "gn", "night night", "nighty night",
        "shubh ratri",                      # Hindi
        "buenas noches",                    # Spanish
        "bonne nuit",                       # French
        "gute nacht",                       # German
        "boa noite",                        # Portuguese
        "buonanotte",                       # Italian
    ],
    "hello": [
        "hello", "hi", "hey", "yo", "sup", "heyy",
        "namaste", "namaskar",              # Hindi
        "hola",                             # Spanish
        "salut",                            # French
        "hallo",                            # German
        "ola",                              # Portuguese
        "ciao",                             # Italian
    ],
}

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
    "cookiefile": os.path.join(BASE_DIR, "cookies.txt") if os.path.exists(os.path.join(BASE_DIR, "cookies.txt")) else None,
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
    if before.status == discord.Status.offline and after.status != discord.Status.offline:

        if after.bot:
            return

        channel = discord.utils.get(
            after.guild.text_channels,
            name="🤗welcome"
        )

        if channel is None:
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


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    user_text = message.content
    username = message.author.display_name
    channel_name = getattr(message.channel, "name", "DM")

    print(f"[{channel_name}] {username}: {user_text}")

    stripped = user_text.strip()
    if stripped and not stripped.startswith(("!", "/")):

        for trigger, keywords in GREETING_KEYWORDS.items():
            if contains_fuzzy_keyword(user_text, keywords):
                response = random.choice(RESPONSES[trigger])
                await message.channel.send(response)
                break

        if contains_fuzzy_keyword(user_text, BLUE_KEYWORDS):

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

        if contains_fuzzy_keyword(user_text, ABHINAV_KEYWORDS):

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


    await bot.process_commands(message)


@bot.tree.command(
    name="playblue",
    description="Play Blue in your voice channel"
)
async def playblue(interaction: discord.Interaction):

    if interaction.user.voice is None:
        await interaction.response.send_message(
            "🔵 Join a voice channel first!"
        )
        return

    await interaction.response.defer()

    channel = interaction.user.voice.channel

    try:

        voice_client = interaction.guild.voice_client

        if voice_client is None:
            voice_client = await channel.connect()

        elif voice_client.channel != channel:
            await voice_client.move_to(channel)

        if voice_client.is_playing():
            voice_client.stop()

        print("Getting audio URL...")

        audio_url = await asyncio.to_thread(
            get_audio_url,
            BLUE_URL
        )

        print("Audio URL obtained.")

        source = discord.FFmpegPCMAudio(
            audio_url,
            **FFMPEG_OPTIONS
        )

        def after_playing(error):
            if error:
                print("Playback error:", error)
            else:
                print("Playback finished.")

        voice_client.play(
            source,
            after=after_playing
        )

        await interaction.followup.send(
            "💙 **BLUE DA BA DEE!** 🎵\n"
            f"Playing in **{channel.name}**!"
        )

    except Exception as e:

        print("================================")
        print("MUSIC ERROR")
        print(e)
        print("================================")

        await interaction.followup.send(
            f"❌ Music failed:\n`{e}`"
        )


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
