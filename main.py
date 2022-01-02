import os
from dotenv import load_dotenv
import logging
from aiogram import Bot, Dispatcher, executor, types
from sp import SpotifyController

state = {
    "page": 0,
    "name": "playlist",
    "description": ""
}

logging.basicConfig(level=logging.INFO)

load_dotenv()

sp_controller = SpotifyController()

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("TELEGRAM_TOKEN_BOT"))
dp = Dispatcher(bot)


# Bot Routes

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.message):
    state["page"] = 1
    await message.answer(
        "Hi, I'm playlist bot, I can transform your text into the playlist in the spotify! \nPlease Enter the name of "
        "the playlist:")


@dp.message_handler(lambda message: state["page"] == 1)
async def input_name(message: types.message):
    state["page"] = 2

    if message.text == "":
        state["page"] = 1
        await message.answer("Name can't be empty, enter at least one symbol please...")
    state["name"] = message.text
    await message.answer("Send me a description: ")


@dp.message_handler(lambda message: state["page"] == 2)
async def input_description(message: types.message):
    state["page"] = 3

    state["description"] = message.text
    print(state)
    await message.answer("Send me a list of songs you want to be added into the spotify playlist")


@dp.message_handler(lambda message: state["page"] == 3)
async def input_songs(message: types.message):
    state["page"] = 4

    if sp_controller.parse_text_and_find_songs(message.text) == 1:
        state["page"] = 3
        await message.answer("Send a list with at least one song in format: Artist - Song")

    await message.answer(f"Your playlist link: {sp_controller.create_a_playlist(state['name'], state['description'])}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
