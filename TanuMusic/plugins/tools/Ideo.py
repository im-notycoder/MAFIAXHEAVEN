# plugins/ideogram_image_plugin.py

import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Configuration
IDEOGRAM_API_KEY = os.getenv("SUOHFi94HRynxgjfmsGSRaKFz3sIehdLGKngNTMSM612u1-bsB-0LuxKUrEExltdbuX0vuee9GeLPyYSfmNUIQ")  # Set your API key as an environment variable
IDEOGRAM_API_URL = "https://api.ideogram.ai/generate"  # Ideogram API endpoint

# Helper Function: Call Ideogram API and Download Image
def generate_image(prompt, category, aspect_ratio="ASPECT_10_16", model="V_2", magic_prompt_option="AUTO"):
    """
    Calls the Ideogram API to generate an image and downloads it locally.
    """
    payload = {
        "image_request": {
            "prompt": f"{category}: {prompt}",  # Add category prefix to the prompt
            "aspect_ratio": aspect_ratio,
            "model": model,
            "magic_prompt_option": magic_prompt_option,
        }
    }
    headers = {
        "Api-Key": IDEOGRAM_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(IDEOGRAM_API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            image_url = result.get("image_url")
            if image_url:
                # Download the image locally
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    file_path = f"downloads/{prompt.replace(' ', '_')[:50]}.jpg"
                    os.makedirs("downloads", exist_ok=True)  # Ensure downloads directory exists
                    with open(file_path, "wb") as file:
                        file.write(image_response.content)
                    return file_path
                else:
                    return {"error": f"Failed to download image. Status: {image_response.status_code}"}
            else:
                return {"error": "Image URL not found in API response."}
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request Exception: {e}"}


# Command: Prompt First, Then Choose Category
@Client.on_message(filters.command("generate_image") & filters.text)
async def generate_image_prompt(client, message):
    """
    Handle `/generate_image` command to get the user's prompt and present category choices.
    """
    if len(message.command) < 2:
        await message.reply("Please provide a prompt to generate an image.\nUsage: `/generate_image <prompt>`")
        return

    # Extract the user's prompt
    prompt = " ".join(message.command[1:])

    # Ask the user to select a category
    await message.reply(
        f"**Prompt received:**\n`{prompt}`\n\nNow choose a category to generate your image:",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Art", callback_data=f"generate|Art|{prompt}")],
                [InlineKeyboardButton("Nature", callback_data=f"generate|Nature|{prompt}")],
                [InlineKeyboardButton("Technology", callback_data=f"generate|Technology|{prompt}")],
                [InlineKeyboardButton("Fantasy", callback_data=f"generate|Fantasy|{prompt}")],
                [InlineKeyboardButton("Sci-Fi", callback_data=f"generate|Sci-Fi|{prompt}")],
            ]
        ),
    )


# Callback: Generate Image Based on Category
@Client.on_callback_query(filters.regex(r"generate\|"))
async def generate_image_category(client, callback_query):
    """
    Handle the category selection to generate an image.
    """
    _, category, prompt = callback_query.data.split("|", 2)

    # Inform the user that the image is being generated
    await callback_query.message.edit_text(
        f"**Generating your {category} image...**\nPrompt: `{prompt}`"
    )

    # Call the API and download the image
    result = generate_image(prompt, category)

    # Handle the response
    if isinstance(result, str):  # File path returned
        try:
            # Send the image with a caption
            await callback_query.message.reply_photo(
                photo=result,
                caption=f"**Category:** {category}\n**Prompt:** {prompt}",
            )
            os.remove(result)  # Clean up the downloaded file
            await callback_query.message.delete()
        except Exception as e:
            await callback_query.message.edit_text(f"Error sending the image: {e}")
    elif "error" in result:
        await callback_query.message.edit_text(f"Error: {result['error']}")
