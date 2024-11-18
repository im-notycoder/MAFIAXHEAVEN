import requests
from pyrogram import Client, filters
from io import BytesIO

# Your API Key for ideogram
API_KEY = "SUOHFi94HRynxgjfmsGSRaKFz3sIehdLGKngNTMSM612u1-bsB-0LuxKUrEExltdbuX0vuee9GeLPyYSfmNUIQ"
url = "https://api.ideogram.ai/generate"

# Define the Pyrogram bot
app = Client("tanu_music_bot")

@app.on_message(filters.command("generate"))
async def generate_image(client, message):
    # Extract the prompt from the user's message
    prompt = message.text.split(' ', 1)  # Split the command and prompt
    if len(prompt) < 2:
        await message.reply("Please provide a prompt after the command. Example: /generate A serene tropical beach scene.")
        return
    
    prompt = prompt[1]  # Get the prompt text after the command
    
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

    # Make the request to the ideogram API
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    # Check if the API responded with an image URL
    if 'image_url' in data:
        # Download the image from the URL
        img_response = requests.get(data['image_url'])
        img = BytesIO(img_response.content)
        
        # Send the image directly to the user
        await message.reply_photo(img, caption="Here is your generated image!")
    else:
        await message.reply("Sorry, something went wrong. Please try again later.")

# Run the bot
app.run()
