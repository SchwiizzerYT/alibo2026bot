import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

TOKEN = os.getenv("BOT_TOKEN", "8989853757:AAEjWcalkvieIBx2Apxl216ZyymaM1nkzrc")

ALPHABET = {
    "o": ("O' o'", "Ö ö"),
    "g": ("G' g'", "Ğ ğ"),
    "sh": ("Sh sh", "Ş ş"),
    "ch": ("Ch ch", "Ç ç"),
}

bot = Bot(token=TOKEN)
dp = Dispatcher()

def letters_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=old, callback_data=f"letter:{key}")
        for key, (old, _new) in ALPHABET.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons[:2], buttons[2:]])

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Assalomu alaykum! Harf tanlang",
        reply_markup=letters_keyboard(),
    )

@dp.callback_query(F.data.startswith("letter:"))
async def show_letter(callback: CallbackQuery):
    key = callback.data.split(":", 1)[1]
    old, new = ALPHABET[key]
    await callback.message.edit_text(
        f"{old}\nYangi alifbodagi yozilishi -> {new}",
        reply_markup=letters_keyboard(),
    )
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.main(main()) if hasattr(asyncio, 'main') else asyncio.run(main())
