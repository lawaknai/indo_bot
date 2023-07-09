from aiogram.dispatcher.filters.state import State, StatesGroup

class UploadStates(StatesGroup):
    TipeKonten = State()
    Konten = State()
    Title = State()
    Description = State()
    UploadButton = State()
    CloseButton = State()
    NonValidContent = State()

    