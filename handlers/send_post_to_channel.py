from aiogram import Bot, types
from aiogram.utils import executor
import requests

def getRandomImage():
    url = 'https://api.waifu.pics/sfw/waifu'

    # Send GET request to the API endpoint
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON data from the response
        data = response.json()
        
        # Access the desired information from the JSON response
        image_url = data['url']
        
        # Do something with the retrieved data
        return image_url
    else:
        # If the request was not successful, print the error status code
        return 'Cannot Find Image'


async def send_photo_from_url_to_channel(bot, channel_id, data):
    photo_url = getRandomImage() # Ganti dengan URL foto yang sesuai
    title = data["title"]
    description = data["description"]
    bot_name = data["bot_name"]
    token = data["token"]
    caption = f"{title}\n{description}\nhttps://t.me/{bot_name}?start={token}"

    # Mengunduh foto dari URL
    try:
        response = requests.get(photo_url)
    except:
        response = None
    photo_path = 'photo.jpg'  # Ganti dengan path foto yang sesuai
    
    with open(photo_path, 'wb') as file:
        try:
            file.write(response.content)
        except:
            file.close()

    # Mengirim foto ke channel dengan caption
    await bot.send_photo(chat_id=channel_id, photo=types.InputFile(photo_path), caption=caption)