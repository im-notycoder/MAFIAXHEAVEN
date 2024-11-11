import random
import logging
import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch

logging.basicConfig(level=logging.INFO)

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def truncate(text):
    list = text.split(" ")
    text1 = ""
    text2 = ""    
    for i in list:
        if len(text1) + len(i) < 30:        
            text1 += " " + i
        elif len(text2) + len(i) < 30:       
            text2 += " " + i

    text1 = text1.strip()
    text2 = text2.strip()     
    return [text1, text2]

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def generate_gradient(width, height, start_color, end_color):
    base = Image.new('RGBA', (width, height), start_color)
    top = Image.new('RGBA', (width, height), end_color)
    mask = Image.new('L', (width, height))
    mask_data = [int(60 * (y / height)) for y in range(height) for _ in range(width)]
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def crop_center_circle(img, output_size, border, border_color, crop_scale=1.5):
    half_the_width = img.size[0] / 2
    half_the_height = img.size[1] / 2
    larger_size = int(output_size * crop_scale)
    img = img.crop(
        (
            half_the_width - larger_size / 2,
            half_the_height - larger_size / 2,
            half_the_width + larger_size / 2,
            half_the_height + larger_size / 2
        )
    )
    img = img.resize((output_size - 2 * border, output_size - 2 * border))
    final_img = Image.new("RGBA", (output_size, output_size), border_color)
    mask_main = Image.new("L", (output_size - 2 * border, output_size - 2 * border), 0)
    draw_main = ImageDraw.Draw(mask_main)
    draw_main.ellipse((0, 0, output_size - 2 * border, output_size - 2 * border), fill=255)
    final_img.paste(img, (border, border), mask_main)
    return final_img

def draw_text_with_shadow(background, draw, position, text, font, fill, shadow_offset=(3, 3), shadow_blur=5):
    shadow = Image.new('RGBA', background.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.text(position, text, font=font, fill="black")
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=shadow_blur))
    background.paste(shadow, shadow_offset, shadow)
    draw.text(position, text, font=font, fill=fill)

async def get_thumb(videoid: str):
    try:
        if os.path.isfile(f"cache/{videoid}_v4.png"):
            return f"cache/{videoid}_v4.png"

        url = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            title = result.get("title", "Unsupported Title")
            title = re.sub("\W+", " ", title).title()
            duration = result.get("duration", "Live")
            thumbnail_data = result.get("thumbnails", [{}])
            thumbnail = thumbnail_data[0].get("url", "").split("?")[0]
            views = result.get("viewCount", {}).get("short", "Unknown Views")
            channel = result.get("channel", {}).get("name", "Unknown Channel")

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                content = await resp.read()
                if resp.status == 200:
                    filepath = f"cache/thumb{videoid}.png"
                    async with aiofiles.open(filepath, mode="wb") as f:
                        await f.write(content)

        image_path = f"cache/thumb{videoid}.png"
        youtube = Image.open(image_path)
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(20))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)

        start_gradient_color = random_color()
        end_gradient_color = random_color()
        gradient_image = generate_gradient(1280, 720, start_gradient_color, end_gradient_color)
        background = Image.blend(background, gradient_image, alpha=0.2)

        draw = ImageDraw.Draw(background)
        arial = ImageFont.truetype("TanuMusic/assets/font2.ttf", 30)
        title_font = ImageFont.truetype("TanuMusic/assets/font3.ttf", 45)

        circle_thumbnail = crop_center_circle(youtube, 400, 20, start_gradient_color)
        circle_thumbnail = circle_thumbnail.resize((400, 400))
        background.paste(circle_thumbnail, (120, 160), circle_thumbnail)

        text_x_position = 565
        title1 = truncate(title)
        draw_text_with_shadow(background, draw, (text_x_position, 180), title1[0], title_font, (255, 255, 255))
        draw_text_with_shadow(background, draw, (text_x_position, 230), title1[1], title_font, (255, 255, 255))
        draw_text_with_shadow(background, draw, (text_x_position, 320), f"{channel}  |  {views[:23]}", arial, (255, 255, 255))

        line_length = 580  
        color_line_percentage = random.uniform(0.15, 0.85) if duration != "Live" else 1.0
        color_line_length = int(line_length * color_line_percentage)
        draw.line([(text_x_position, 380), (text_x_position + color_line_length, 380)], fill=random_color(), width=9)

        draw_text_with_shadow(background, draw, (text_x_position, 400), "00:00", arial, (255, 255, 255))
        draw_text_with_shadow(background, draw, (1080, 400), duration, arial, (255, 255, 255))

        os.remove(f"cache/thumb{videoid}.png")
        background_path = f"cache/{videoid}_v4.png"
        background.save(background_path)

        return background_path

    except Exception as e:
        logging.error(f"Error generating thumbnail for video {videoid}: {e}")
        return None
