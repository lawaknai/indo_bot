from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_tipe_konten_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔗 Link", callback_data="link"),
        InlineKeyboardButton("🖼️ Gambar", callback_data="gambar"),
        InlineKeyboardButton("🎥 Video", callback_data="video"),
        InlineKeyboardButton("❌ Batal", callback_data="batal")
    )
    return keyboard

def get_non_valid_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔄 Input Ulang", callback_data="input_ulang"),
        InlineKeyboardButton("❌ Keluar dari obrolan", callback_data="exit"))
    return keyboard

def get_one_exit_button(payload):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(f"🍎 set sebagai tanpa {payload}", callback_data="non"))
    return keyboard

def upload_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(f"🍌 upload content", callback_data="upload"),
                 InlineKeyboardButton(f"🐒 batal upload", callback_data="batal_upload")
                 )
    return keyboard

def get_exit_button():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(f"❌ atau exit?", callback_data="exit"))
    return keyboard