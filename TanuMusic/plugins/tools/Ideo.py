import asyncio
from pyrogram import Client, filters
import requests
from io import BytesIO
from TanuMusic import app 

API_KEY = "SUOHFi94HRynxgjfmsGSRaKFz3sIehdLGKngNTMSM612u1-bsB-0LuxKUrEExltdbuX0vuee9GeLPyYSfmNUIQ"
url = "https://api.ideogram.ai/generate"

@app.on_message(filters.command("generate"))
async def generate_image(client, message):
    prompt = message.text.split(' ', 1)
    if len(prompt) < 2:
        await message.reply("Please provide a prompt after the command. Example: /generate A serene tropical beach scene.")
        return

    prompt = prompt[1]

    payload = {
        "image_request": {
            "prompt": prompt,
            "aspect_ratio": "ASPECT_10_16",
            "model": "V_2",
            "magic_prompt_option": "AUTO"
        }
    }

    headers = {
        "Api-Key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    if 'image_url' in data:
        img_response = requests.get(data['image_url'])
        img = BytesIO(img_response.content)
        await message.reply_photo(img, caption="Here is your generated image!")
    else:
        await message.reply("Sorry, something went wrong. Please try again later.")
