import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

#❖ Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID", "27077018"))
API_HASH = getenv("API_HASH", "4b4ffeda4f29a8268202ca6b61b5c654")

#❖ Add Owner Username without @ 
OWNER_USERNAME = getenv("OWNER_USERNAME", "dark_seraphim_00")

#❖  Get Your bot username
BOT_USERNAME = getenv("BOT_USERNAME", "DynamicMusicXBot")

#❖  Don't Add style font 
BOT_NAME = getenv("BOT_NAME", "𝑫𝒚𝒏𝒂𝒎𝒊𝒄 ✗ 𝑴𝒖𝒔𝒊𝒄™")

#❖ get Your Assistant User name
ASSUSERNAME = getenv("ASSUSERNAME", "𝑫𝒚𝒏𝒂𝒎𝒊𝒄 ✗ 𝑨𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕")

#❖ Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN", "8164404114:AAFKm8xETsR6KbkfCBPsQHNiVoCXf9o9-98")

#❖ Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://EXONTESTMONGO:EXONTESTMONGO@cluster0.bviw7ic.mongodb.net/?retryWrites=true&w=majority")

# Vars For API End Pont.
API_URL = getenv("API_URL", 'https://api.thequickearn.xyz') #youtube song url
API_KEY = getenv("API_KEY", "NxGBNexGenBots26f6e9") # youtube song api key, get it from https://t.me/RahulTC

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 600000))

#❖  Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID", "-1002093750764"))

#❖ Get this value from @FallenxBot on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", "7991835680"))

#❖  Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", None)

#❖  Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY", None)

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/im-notycoder/MAFIAXHEAVEN",
)

UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")

GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  #❖ Fill this variable if your upstream repository is private

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/DynamicXNetwork")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/DynamicXSupport")

#❖ Set this to True if you want the assistant to automatically leave chats after an interval
AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False))


#❖ Get this credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "e319091f771445b18c029299505d5d4f")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "293c334a2861415197a697b2d11dd4de")


#❖ Maximum limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 2500))


#❖ Telegram audio and video file size limit (in bytes)
TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))
#❖ Checkout https://www.gbmb.org/mb-to-bytes for converting mb to bytes


#❖ Get your pyrogram v2 session from @StringFatherBot on Telegram
STRING1 = getenv("STRING_SESSION", "BQGdKZoATRlR7zq-R2qjnm-XZD_xxPchllX0BxCYw-z1VYe1qm_L1DA8uobinHrRjJXuaRvQTf4n4axPTMmKFasRkiVL5ydgB5lNkd9Dab6AEfkN0cG9G0kMjznbQ6H-n6RJkYNIxifR5qbYwna9WkRctxZKe15kTbqzLEREjUu-b8CB-GHY5SGRvBGwV-lwilbiiTjWiSWSpUmxCjyiENDv6MPotBaYnxvRNE8jLsJBiyl-C13CvouKhvIJuXvgOMQSl92xdfyxC_vwnhU1S9EXCBADwlMhazFnqeuyD2I5qzJiUgG1fokRujt_2h2zsvj0uVoHKC0gVm4V7dURk1XHFIIeMAAAAAHCTUmHAA")
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}


START_IMG_URL = getenv(
    "START_IMG_URL", "https://files.catbox.moe/rc83dq.jpg"
)
PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://envs.sh/qEB.jpg"
)
PLAYLIST_IMG_URL = "https://telegra.ph/file/7795e58425337d0455e95.jpg"
STATS_IMG_URL = "https://i.ibb.co/xmxBfGm/photo-2024-11-19-14-16-17-7438994282792353840.jpg"
TELEGRAM_AUDIO_URL = "https://telegra.ph/file/d2081243af7c1d7578b7b.jpg"
TELEGRAM_VIDEO_URL = "https://telegra.ph/file/d2081243af7c1d7578b7b.jpg"
STREAM_IMG_URL = "https://telegra.ph/file/982b01ba53c3d69b0d0ce.jpg"
SOUNCLOUD_IMG_URL = "https://telegra.ph/file/982b01ba53c3d69b0d0ce.jpg"
YOUTUBE_IMG_URL = "https://telegra.ph/file/d2081243af7c1d7578b7b.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://telegra.ph/file/61024698bfc926e95d57a.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://telegra.ph/file/61024698bfc926e95d57a.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://telegra.ph/file/61024698bfc926e95d57a.jpg"
FAILED = "https://graph.org/file/40581c7048b1ee71209a2-3fc027862ecf64213d.jpg"



def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
)
