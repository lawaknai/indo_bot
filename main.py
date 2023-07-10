from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


from states.states import UploadStates
from template import Response, get_tipe_konten_keyboard, upload_response_text, get_non_valid_keyboard,get_one_exit_button,upload_keyboard,get_exit_button
from utils import logger, get_data,check_link_validity, normalize_data,get_new_info
from handlers.send_post_to_channel import send_photo_from_url_to_channel
from db.sqllite_connection import DatabaseManager

from dotenv import load_dotenv
import os

# Memuat variabel lingkungan dari file .env
load_dotenv()


# Inisialisasi bot dan dispatcher
try:
    bot = Bot(token=os.getenv('TOKEN_API'))
    BOT_NAME = os.getenv('BOT_NAME')
    CHANNEL = os.getenv('CHANNEL')
    channel_target = os.getenv("CHANNEL_NAME")
    dp = Dispatcher(bot, storage=MemoryStorage())
    db_manager = DatabaseManager('database.db')
except Exception as e:
    logger.error(e)

@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    logger.debug(f"COMMAND START DIMULAi {message}")
    try:
        # Tanggapan ketika pengguna mengetikkan /start
        x = message.get_args()
        data = db_manager.get_content([x])
        if data is None:
            return
        logger.debug(f"GET DATA DARI DB {data}")
        if data[0] == 'link':
            content = data[1]
            await message.reply(f"Silahkan Klik Linknya bos: {content}")
        if data[0]== 'gambar':
            await bot.send_photo(chat_id=message.chat.id, photo=data[1])
        if data[0]== 'video':
            logger.debug(f"CEK VIDEO ID: {data}")
            await bot.send_video(chat_id=message.chat.id, video=data[1])
    except Exception as e:
        if 'state' in locals():
            state.finish()
        logger.error(e)
    
# Handler untuk perintah /upload
@dp.message_handler(Command("upload"))
async def cmd_upload(message: types.Message):
    try:
        args = message.get_args()
        if args != "labalabagabisaberenang":
            return
        # Mulai dengan state TipeKonten
        logger.debug(f"UPLOAD MESSAGE: {message}")
        uname = message["from"]["first_name"]
        await message.reply(upload_response_text(uname), reply_markup=get_tipe_konten_keyboard())
        await UploadStates.TipeKonten.set()
    except Exception as e:
        if 'state' in locals():
            await state.finish()
        logger.error(e)

# Handler untuk pemilihan tipe konten
@dp.callback_query_handler(Text(equals=["link", "gambar", "video", "batal"]), state=UploadStates.TipeKonten)
async def process_tipe_konten(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        # Dapatkan pilihan tipe konten dari callback_data
        tipe_konten = callback_query.data
        # Update state dengan tipe konten yang dipilih
        await state.update_data(tipe_konten=tipe_konten)
        # Tampilkan respons sesuai dengan tipe konten yang dipilih
        keyboard = get_exit_button()
        if tipe_konten == "link":
            await bot.send_message(callback_query.from_user.id, "[LINK] drop link nya suhu",reply_markup=keyboard)
            await UploadStates.Konten.set()
        elif tipe_konten == "gambar":
            await bot.send_message(callback_query.from_user.id, "[GAMBAR] drop gambarnya suhu / foward dari chat lain",reply_markup=keyboard)
            await UploadStates.Konten.set()
        elif tipe_konten == "video":
            await bot.send_message(callback_query.from_user.id, "[VIDEO] drop video nya suhu / foward dari chat lain",reply_markup=keyboard)
            await UploadStates.Konten.set()
        elif tipe_konten == "batal":
            await bot.send_message(callback_query.from_user.id, "See you next time suhu")
            await state.finish()
    except Exception as e:
        if 'state' in locals():
            await state.finish()
        logger.error(e)
    
# CANCEL 
@dp.callback_query_handler(Text(equals=["exit"]), state=UploadStates.Konten)
async def process_non_valid_content(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.send_message(callback_query.from_user.id, "See you next time suhu")
        await state.finish()
    except Exception as e:
        if 'state' in locals():
            await state.finish()
        logger.error(e)
  
@dp.message_handler(state=UploadStates.Konten)
async def process_link(message: types.Message, state: FSMContext):
    try:
        x = await state.get_data()
        logger.debug(f"CEK DATA LINK: {x}")
        y = x["tipe_konten"]
        if (y == 'link'):
            if (check_link_validity(message.text) == False):
                await bot.send_message(message.from_user.id, f"Kayak nya input linknya gak valid dah", reply_markup=get_non_valid_keyboard())
                await UploadStates.NonValidContent.set()
            else:     
                await state.update_data(konten=message.text)
                await bot.send_message(message.from_user.id, "ketik judul konten nya suhu! ", reply_markup=get_one_exit_button('judul'))
                await UploadStates.Title.set()
        else :
            await bot.send_message(message.from_user.id, f"Input {y} tidak valid", reply_markup=get_non_valid_keyboard())
            await UploadStates.NonValidContent.set()
    except Exception as e:
        if 'state' in locals():
            await state.finish()
        logger.error(e)
        
# NonValidContent
@dp.callback_query_handler(Text(equals=["input_ulang", "exit"]), state=UploadStates.NonValidContent)
async def process_non_valid_content(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        opsi = callback_query.data
        x = await state.get_data()
        y = x["tipe_konten"]
        logger.debug(f"CEK NONVALID DATA: {callback_query}")
        if opsi == "input_ulang":
            await bot.send_message(callback_query.from_user.id, f"silahkan input {y} yang valid suhu")
            await state.set_state(UploadStates.Konten)
        if opsi == "exit":
            await bot.send_message(callback_query.from_user.id, f"See you next time suhu")
            await state.finish()
    except Exception as e:
        if 'state' in locals():
            await state.finish()
        logger.error(e)
        
# Handler untuk memproses gambar
@dp.message_handler(content_types=types.ContentType.PHOTO, state=UploadStates.Konten)
async def process_gambar(message: types.Message, state: FSMContext):
    try:
        validation = await state.get_data()
        if validation['tipe_konten'] != 'gambar':
            await bot.send_message(message.from_user.id, f"Kayak nya inputan gak valid dah", reply_markup=get_non_valid_keyboard())
            await UploadStates.NonValidContent.set()
        else:
            file_id = message.photo[-1].file_id
            logger.debug(f"DEBUG DATA PHOTO: {message}")
            # Lakukan pemrosesan gambar sesuai kebutuhan
            # Misalnya, menyimpan file_id ke database, dsb.

            await bot.send_message(message.from_user.id, "Gambar berhasil diunggah!")
            await bot.send_message(message.from_user.id, "ketik judul konten nya suhu! ", reply_markup=get_one_exit_button('judul'))
            await state.update_data(konten=file_id)
            await UploadStates.Title.set()
    except Exception as e:
        if 'state' in locals():
            await state.finish()
        logger.error(e)


# Handler untuk memproses video
@dp.message_handler(content_types=types.ContentType.VIDEO, state=UploadStates.Konten)
async def process_video(message: types.Message, state: FSMContext):
    try:
        logger.debug(f"CEK DATA VIDEO {message}")
        file_id = message.video.file_id
        video_duration = message.video.duration
        video_file_name = message.video.file_name
        video_thumbnail = message.video["thumbnail"]["file_id"]
        video_thumb = message.video["thumb"]["file_id"]
        # Lakukan pemrosesan video sesuai kebutuhan
        # Misalnya, menyimpan file_id ke database, dsb.

        await bot.send_message(message.from_user.id, "Video berhasil diunggah!")
        await bot.send_message(message.from_user.id, "ketik judul konten nya suhu! ", reply_markup=get_one_exit_button('judul'))
        await state.update_data(konten=file_id)
        await state.update_data(video_duration=video_duration)
        await state.update_data(video_file_name=video_file_name)
        await state.update_data(video_thumbnail=video_thumbnail)
        await state.update_data(video_thumb=video_thumb)
        await UploadStates.Title.set()
    except Exception as e:
        if 'state' in locals():
            await state.finish()
        logger.error(e)
    
# TITLE HANDLERS:
@dp.callback_query_handler(Text(equals=["non"]), state=UploadStates.Title)
async def process_non_title(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.send_message(callback_query.from_user.id, "ketik Decription konten nya suhu! ", reply_markup=get_one_exit_button('Decription'))
        await UploadStates.Description.set()
    except Exception as e:
        if 'state' in locals():
            await state.finish()
        logger.error(e)
    
@dp.message_handler(state=UploadStates.Title)
async def process_title(message: types.Message, state: FSMContext):
    try:
        await state.update_data(title=message.text)
        await bot.send_message(message.from_user.id, "ketik Decription konten nya suhu! ", reply_markup=get_one_exit_button('Decription'))
        await UploadStates.Description.set()
    except Exception as e:
        if 'state' in locals():
            await state.finish()
        logger.error(e)
            
    
# DescriptionHandler
@dp.callback_query_handler(Text(equals=["non"]), state=UploadStates.Description)
async def process_non_description(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.send_message(callback_query.from_user.id, "pilih langkah selanjutnya suhu", reply_markup=upload_keyboard())
        await UploadStates.UploadButton.set()
    except Exception as e:
        if 'state' in locals():
            await state.finish()
        logger.error(e)

@dp.message_handler(state=UploadStates.Description)
async def process_description(message: types.Message, state: FSMContext):
    try:
        await state.update_data(description=message.text)
        await bot.send_message(message.from_user.id, "pilih langkah selanjutnya suhu", reply_markup=upload_keyboard())
        await UploadStates.UploadButton.set()
    except Exception as e:
        if 'state' in locals():
            await state.finish()
        logger.error(e)
    
@dp.callback_query_handler(Text(equals=["batal_upload"]),state=UploadStates.UploadButton)
async def upload_cancel(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.send_message(callback_query.from_user.id, "see you next time suhu!")
    except Exception as e:
        if 'state' in locals():
            await state.finish()
        logger.error(e)
    
@dp.callback_query_handler(Text(equals=["upload"]),state=UploadStates.UploadButton)
async def process_upload(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        logger.debug(f"FINAL DATA {message}:")
        normalization_data = normalize_data(data)
        logger.debug(f"NORMALIZATION DATA {normalization_data}:")
        token = get_new_info(normalization_data)
        logger.debug(f"GET TOKEN {token}")
        caption = {
            "title": normalization_data["title"],
            "description": normalization_data["description"],
            "bot_name": BOT_NAME,
            "token": token[0]
        }
        from_id = message["from"]["id"]
        
        await bot.send_message(message.from_user.id, f"wait.. lagi di proses ")
        db_manager.insert_content([normalization_data["content_type"], token[0], token[1],from_id])
        await send_photo_from_url_to_channel(bot,CHANNEL, caption)
        await bot.send_message(message.from_user.id, f"SUCCESS 🍌🍎.\nMerci Monsieur!\npasse une bonne journée\nKonten diupload ke {channel_target}")
        await state.finish()

    except Exception as e:
        if 'state' in locals():
            await state.finish()
        logger.error(e)
        
# Jalankan bot
if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(dp.start_polling())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(dp.storage.close())
        loop.run_until_complete(dp.storage.wait_closed())
        loop.close()
