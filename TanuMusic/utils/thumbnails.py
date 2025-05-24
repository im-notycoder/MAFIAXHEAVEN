import os
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat
from youtubesearchpython.__future__ import VideosSearch
from config import FAILED

# Constants
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

WIDTH, HEIGHT = 1280, 720
CARD_WIDTH, CARD_HEIGHT = 1000, 580
CARD_RADIUS = 54
PADDING_X, PADDING_Y = 140, 80

FONT_TITLE = "TanuMusic/assets/font.ttf"
FONT_SUB = "TanuMusic/assets/font2.ttf"

def truncate_text(text, font, max_width):
    if font.getlength(text) <= max_width:
        return text
    truncated = text
    while font.getlength(truncated + "...") > max_width and truncated:
        truncated = truncated[:-1]
    return truncated + "..." if truncated else "..."

def get_average_color(image: Image.Image) -> tuple:
    small = image.resize((50, 50))
    stat = ImageStat.Stat(small)
    return tuple(int(c) for c in stat.mean[:3])

async def get_thumb(videoid: str) -> str:
    cache_path = os.path.join(CACHE_DIR, f"{videoid}_musiccard.jpg")
    if os.path.exists(cache_path):
        return cache_path

    try:
        results = VideosSearch(videoid, limit=1)
        data = (await results.next())["result"][0]
        title = data.get("title", "Unknown Title")
        channel = data.get("channel", {}).get("name", "Unknown Channel")
        thumbnail = data.get("thumbnails", [{}])[0].get("url", FAILED)
        views = data.get("viewCount", {}).get("text", "0 views")
    except Exception:
        title, channel, thumbnail, views = "Unknown Title", "Unknown Channel", FAILED, "0 views"

    thumb_path = os.path.join(CACHE_DIR, f"thumb_{videoid}.png")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(thumb_path, "wb") as f:
                        await f.write(await resp.read())
                else:
                    return FAILED
    except Exception:
        return FAILED

    try:
        # Load album art
        album_art_raw = Image.open(thumb_path).convert("RGB")

        # Background = blurred album art
        bg = album_art_raw.resize((WIDTH, HEIGHT)).filter(ImageFilter.GaussianBlur(24))
        draw = ImageDraw.Draw(bg)

        # Auto card color based on album art average
        avg_color = get_average_color(album_art_raw)
        card_color = tuple(int(c * 0.6) for c in avg_color)  # darken for contrast

        # Card base
        card = Image.new("RGBA", (CARD_WIDTH, CARD_HEIGHT), (0, 0, 0, 0))
        card_draw = ImageDraw.Draw(card)
        card_draw.rounded_rectangle((0, 0, CARD_WIDTH, CARD_HEIGHT), radius=CARD_RADIUS, fill=card_color)

        # Album Art
        art_box = (60, 40, CARD_WIDTH - 60, 440)
        art_width = art_box[2] - art_box[0]
        art_height = art_box[3] - art_box[1]
        album_art = album_art_raw.resize((art_width, art_height))
        mask = Image.new("L", (art_width, art_height), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, art_width, art_height), radius=40, fill=255)
        card.paste(album_art, (art_box[0], art_box[1]), mask)

        # Fonts
        try:
            title_font = ImageFont.truetype(FONT_TITLE, 46)
            meta_font = ImageFont.truetype(FONT_SUB, 32)
        except:
            title_font = meta_font = ImageFont.load_default()

        # Text
        text_y = art_box[3] + 25
        text_x = art_box[0]
        max_title_width = CARD_WIDTH - 120

        short_title = truncate_text(title, title_font, max_title_width)
        card_draw.text((text_x, text_y), short_title, font=title_font, fill=(255, 255, 255))
        card_draw.text((text_x, text_y + 55), f"{channel} • {views}", font=meta_font, fill=(220, 220, 220))

        # Progress bar
        bar_y = CARD_HEIGHT - 45
        card_draw.rounded_rectangle((text_x, bar_y, text_x + max_title_width, bar_y + 8), radius=4, fill=(120, 120, 120))
        card_draw.rounded_rectangle((text_x, bar_y, text_x + 360, bar_y + 8), radius=4, fill=(255, 0, 180))
        card_draw.ellipse((text_x + 350, bar_y - 5, text_x + 370, bar_y + 15), fill=(255, 0, 180))

        # Paste card onto background
        mask_card = Image.new("L", (CARD_WIDTH, CARD_HEIGHT), 0)
        ImageDraw.Draw(mask_card).rounded_rectangle((0, 0, CARD_WIDTH, CARD_HEIGHT), radius=CARD_RADIUS, fill=255)
        bg.paste(card, (PADDING_X, PADDING_Y), mask_card)

        os.remove(thumb_path)
        bg.save(cache_path, format="JPEG", quality=95)
        return cache_path

    except Exception as e:
        print(f"Thumbnail generation failed: {e}")
        return FAILED
