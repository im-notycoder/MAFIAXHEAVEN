import requests
from pyrogram import Client, filters
from pyrogram.types import Message

# Function to generate an image based on the user's prompt
def generate_image(prompt: str):
    # Replace these with your actual Ideogram API Key and URL
    url = "https://api.ideogram.ai/generate"
    headers = {
        "Api-Key": "SUOHFi94HRynxgjfmsGSRaKFz3sIehdLGKngNTMSM612u1-bsB-0LuxKUrEExltdbuX0vuee9GeLPyYSfmNUIQ",  # Replace with your Ideogram API key
        "Content-Type": "application/json"
    }

    payload = {
        "image_request": {
            "prompt": prompt,
            "aspect_ratio": "ASPECT_10_16",
            "model": "V_2",
            "magic_prompt_option": "AUTO"
        }
    }

    # Make the API request
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        # Get the image URL from the response
        image_url = response.json().get('image_url')
        return image_url
    else:
        return None

# Define the /generate command plugin
async def generate_command(client, message: Message):
    # Check if the message starts with "/generate"
    if message.text.startswith("/generate"):
        # Extract the prompt from the user's message
        prompt = message.text[len("/generate "):].strip()
        
        if not prompt:
            # If no prompt is provided, send an error message
            await message.reply_text("Please provide a prompt after /generate command. Example: /generate A futuristic city.")
            return
        
        # Generate the image based on the prompt
        image_url = generate_image(prompt)

        if image_url:
            # Send the generated image to the user
            await message.reply_photo(photo=image_url, caption=f"Here is your generated image for the prompt: {prompt}")
        else:
            # If image generation fails
            await message.reply_text("Sorry, I couldn't generate the image. Please try again later.")

# Add this plugin to your bot (assuming you have a running Pyrogram Client)
def add_generate_plugin(app):
    app.add_handler(filters.command("generate")(generate_command))
